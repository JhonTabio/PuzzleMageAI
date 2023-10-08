import cv2
import numpy as np
import tensorflow as tf
from backend.sudoku import Validator, Solver
from flask import Flask, Response, render_template
from flask_cors import CORS

model = tf.keras.models.load_model("backend/model/digit_ocr.h5")
show_border = False
border_color = (0, 0, 255)
number_color = (119, 0, 95)

def create_rounded_mask(shape, radius):
    """
    Creates a mask with rounded corners for an image.
    :param shape: tuple, the shape of the mask (height, width).
    :param radius: int, the radius of the rounded corners.
    :return: numpy array, the mask with rounded corners.
    """
    height, width = shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    # Draw the four corners
    cv2.circle(mask, (radius, radius), radius, 255, -1)
    cv2.circle(mask, (width - radius, radius), radius, 255, -1)
    cv2.circle(mask, (radius, height - radius), radius, 255, -1)
    cv2.circle(mask, (width - radius, height - radius), radius, 255, -1)

    # Draw the rectangle for the main body and sides
    cv2.rectangle(mask, (radius, 0), (width - radius, height), 255, -1)
    cv2.rectangle(mask, (0, radius), (width, height - radius), 255, -1)

    return mask


def set_number_color(color: tuple):
    number_color = color

def set_border_color(color: tuple):
    border_color = color

def set_show_border(value: bool):
    show_border = value

def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    adapt_thresh_inv = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    opening = cv2.morphologyEx(adapt_thresh_inv, cv2.MORPH_OPEN, kernel)
    return opening


def find_largest_contour(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    largest_contour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            if area > max_area:
                max_area = area
                largest_contour = contour
    return largest_contour


def get_corners(largest_contour):
    coords = np.zeros((4, 2), np.float32)
    sumation = largest_contour.sum(axis=2)
    coords[0] = largest_contour[np.argmin(sumation)][0]
    coords[2] = largest_contour[np.argmax(sumation)][0]
    difference = np.diff(largest_contour, axis=2)
    coords[1] = largest_contour[np.argmin(difference)][0]
    coords[3] = largest_contour[np.argmax(difference)][0]
    return coords


def validate_rect(coords):
    tleft, tright, bright, bleft = coords

    widthTop = np.sqrt(((tright[0] - tleft[0]) ** 2) + ((tright[1] - tleft[1]) ** 2))
    widthBot = np.sqrt(((bright[0] - bleft[0]) ** 2) + ((bright[1] - bleft[1]) ** 2))

    heightRight = np.sqrt(
        ((tright[0] - bright[0]) ** 2) + ((tright[1] - bright[1]) ** 2)
    )
    heightLeft = np.sqrt(((tleft[0] - bleft[0]) ** 2) + ((tleft[1] - bleft[1]) ** 2))

    deltaH = 0.2 * max(heightLeft, heightRight)
    deltaW = 0.2 * max(widthBot, widthTop)

    if abs(widthTop - widthBot) < deltaW and abs(heightRight - heightLeft) < deltaH:
        return True
    return False


def perspective_transform(coords, image):
    tleft, tright, bright, bleft = coords

    widthTop = np.sqrt(((tright[0] - tleft[0]) ** 2) + ((tright[1] - tleft[1]) ** 2))
    widthBot = np.sqrt(((bright[0] - bleft[0]) ** 2) + ((bright[1] - bleft[1]) ** 2))
    maxWidth = max(int(widthBot), int(widthTop))

    heightRight = np.sqrt(
        ((tright[0] - bright[0]) ** 2) + ((tright[1] - bright[1]) ** 2)
    )
    heightLeft = np.sqrt(((tleft[0] - bleft[0]) ** 2) + ((tleft[1] - bleft[1]) ** 2))
    maxHeight = max(int(heightRight), int(heightLeft))

    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    M = cv2.getPerspectiveTransform(coords, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def remove_border(binary_image):
    x = binary_image.shape[1]
    y = binary_image.shape[0]
    border = int(0.12 * x)
    roi = binary_image[border : y - border, border : x - border]
    return roi


def empty(image):
    if cv2.countNonZero(image) >= 0.97 * (image.shape[0] * image.shape[1]):
        return True
    else:
        return False


def get_board(grid):
    grid_resized = grid.copy()
    grid_resized = cv2.resize(
        grid_resized, (grid_resized.shape[0], grid_resized.shape[0]), cv2.INTER_AREA
    )
    posx = grid_resized.shape[1] // 9
    posy = grid_resized.shape[0] // 9
    border = 3
    digitSize = 32
    sudoku = np.zeros((9, 9), dtype=np.uint8)

    for i in range(9):
        for j in range(9):
            digit = grid_resized[posy * i : posy * (i + 1), posx * j : posx * (j + 1)]

            thresholdY = int(0.25 * digit.shape[1])
            thresholdX = int(0.25 * digit.shape[0])
            center = digit[
                thresholdY : digit.shape[1] - thresholdY,
                thresholdX : digit.shape[0] - thresholdX,
            ]
            if empty(center):
                continue
            else:
                crop_image = remove_border(digit)
                resize = cv2.resize(
                    crop_image,
                    (digitSize - 2 * border, digitSize - 2 * border),
                    cv2.INTER_AREA,
                )
                padded_digit = cv2.copyMakeBorder(
                    resize,
                    border,
                    border,
                    border,
                    border,
                    cv2.BORDER_CONSTANT,
                    value=(255, 255, 255),
                )
                padded_digit = padded_digit.astype("float32")
                padded_digit = padded_digit / 255.0
                pred = (
                    model.predict(
                        padded_digit.reshape(1, digitSize, digitSize, 1)
                    ).argmax(axis=1)[0]
                    + 1
                )
                sudoku[i][j] = pred

    return sudoku


def fill_board(solved, unsolved, image):
    gridw = image.shape[1]
    gridh = image.shape[0]

    xgap = gridw // 9
    ygap = gridh // 9
    margin = int(0.015 * image.shape[1])

    for i in range(9):
        for j in range(9):
            if unsolved[i][j] == 0:
                text = str(solved[i][j])
                xloc = xgap * j + margin
                yloc = ygap * (i + 1) - margin
                fontsize = gridw / 400
                cv2.putText(
                    image,
                    text,
                    (xloc, yloc),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontsize,
                    number_color,
                    2,
                )

    return image

def unwarp_image(image_src, image_dest, pts_dest):
    pts_dest = np.array(pts_dest)

    height, width = image_src.shape[0], image_src.shape[1]
    pts_source = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype="float32",
    )
    h, status = cv2.findHomography(pts_source, pts_dest)
    warped = cv2.warpPerspective(
        image_src, h, (image_dest.shape[1], image_dest.shape[0])
    )
    cv2.fillConvexPoly(image_dest, pts_dest.astype("int32"), 0)

    image = cv2.add(image_dest, warped)

    return image

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    cap = cv2.VideoCapture(2)
    sudoku_matrix = np.zeros((9, 9), dtype=np.uint8)
    validation = False

    while cap.isOpened():
        ret, frame = cap.read()

        # Ensure frame has 4 channels (BGRA)
        if frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        mask = create_rounded_mask(frame.shape[:2], 50)

        # Set the alpha channel using the mask
        frame[:, :, 3] = mask

        processedFrame = preprocess(frame)
        largest_contour = find_largest_contour(processedFrame)

        try:
            coords = get_corners(largest_contour)
            if validate_rect(coords):
                if show_border:
                    cv2.drawContours(frame, [largest_contour], 0, border_color, 2)

                warped = perspective_transform(coords, frame)
                warped_binary = preprocess(warped)
                warped_inv = cv2.bitwise_not(warped_binary)

                if not validation:
                    sudoku_matrix = get_board(warped_inv)
                    unsolved = sudoku_matrix.copy()
                    if (
                        Validator().is_valid_board(sudoku_matrix)
                        and np.count_nonzero(sudoku_matrix) != 0
                    ):
                        validation = True
                        sudoku_matrix = Solver().solve_wrapper(sudoku_matrix)
                solved_grid_image = fill_board(sudoku_matrix, unsolved, warped)
                frame = unwarp_image(solved_grid_image, frame, coords)

        except:
            pass

        _, jpeg = cv2.imencode('.png', frame)  # Use PNG format to support transparency
        yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
