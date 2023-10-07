"""
    Image Processing functions

    By: Jhon Tabio
"""
import cv2
import numpy as np
import numpy.typing as npt
from boards.sudoku import Sudoku

def process_image(img: np.ndarray) -> tuple[bool, npt.NDArray[any]]: # Return function success and image
    """
        Takes in and processes image data, outlines and returns
        a simplified version of the image.

        Args:
            img: Image
        Return:
            tuple: Size 2, first index returns whether the function was sucessful
                second index returns the modified image
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert our image to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # Apply a blur to our image
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # Apply a threshold to our image
                                   cv2.THRESH_BINARY_INV, 11, 2)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, # Find all contours in our image
                                cv2.CHAIN_APPROX_SIMPLE)[0]

    if contours == None: # If no contours, we have no interest
        return False, None

    max_cnt = max(contours, key=cv2.contourArea) # Store our largest contour

    if cv2.contourArea(max_cnt) < 250 * 250: # Check if the contour is greater than 250 ** 2 pixel squared
        return False, None

    mask = np.zeros(gray.shape, np.uint8) # Generate a black mask
    cv2.drawContours(mask, [max_cnt], 0, 255, -1) # Fill within contours all white
    cv2.drawContours(mask, [max_cnt], 0, 0, 2) # The rest is filled with black

    out = 255 * np.ones_like(gray) # Generate a white mask
    out[mask == 255] = gray[mask == 255]

    aligned_image, matrix = align_image(out, max_cnt)

    detect_board(aligned_image)

    return True, aligned_image

def align_image(img: np.ndarray, max_cnt):
    """
        Apply a perspective tranformation by finding the corners of the contour to convert the
        image from being skewed to a straight image

        Args:
            img: Input image
    """

    peri = cv2.arcLength(max_cnt, True) # Calculate the perimeter of our contour
    approx = cv2.approxPolyDP(max_cnt, 0.015 * peri, True) # Calculate and approximate the polygonal curves to detect our verticies
    pts = np.squeeze(approx) # Flatten the verticies array
    box_width = np.max(pts[:, 0]) - np.min(pts[:, 0]) # Grab the width
    box_height = np.max(pts[:, 1]) - np.min(pts[:, 1]) # Grab the height

    """
        The following steps are used to approximate the corner coordinates of the image
        in order to apply an appropriate transformation.
    """

    sum_pts = pts.sum(axis=1)
    diff_pts = np.diff(pts, axis=1)
    bounding_rect = np.array([pts[np.argmin(sum_pts)],
                                pts[np.argmin(diff_pts)],
                                pts[np.argmax(sum_pts)],
                                pts[np.argmax(diff_pts)]], dtype=np.float32)

    dst = np.array([[0, 0],
                    [box_width - 1, 0],
                    [box_width - 1, box_height - 1],
                    [0, box_height - 1]], dtype=np.float32)

    transform_matrix = cv2.getPerspectiveTransform(bounding_rect, dst) # Create the transformation matrix
    transformed_img = cv2.warpPerspective(img, transform_matrix, (box_width, box_height)) # Apply the transformed matrix to our image

    return transformed_img, transform_matrix

def detect_board(img: np.ndarray):
    # TODO: Determine different board types
    sudoku = Sudoku(img)
