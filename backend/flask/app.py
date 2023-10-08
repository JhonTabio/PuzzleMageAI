from flask import Flask, render_template, Response
import cv2 as cv

app = Flask(__name__)

camera = cv.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break # no frame, break loop
        else:
            ret, buffer = cv.imencode('.jpg', frame) # encode the frame in JPEG format
            frame = buffer.tobytes() # buffer convert to bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
