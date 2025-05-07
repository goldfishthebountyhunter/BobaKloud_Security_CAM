# server_camera.py (Flask backend)
import cv2
from flask import Flask, Response

app = Flask(__name__)

def gen():
    cam = cv2.VideoCapture(0)  # Access server webcam
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>Server Webcam</h1>
        <img src="/video_feed">
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)