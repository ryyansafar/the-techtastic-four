from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# OpenCV video capture
video_capture = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Capture frames from the webcam
        success, frame = video_capture.read()
        if not success:
            break

        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/')
def output():
    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001)
