import cv2
from ultralytics import YOLO
from flask import Flask, request, Response, redirect, render_template
from uuid import uuid4
import os
import time
import threading

# Create uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# Load the YOLO model (assuming it's trained for 'fire' and 'smoke' detection)
model = YOLO("weights/best.pt")

app = Flask(__name__, template_folder='templates', static_folder='static')

# Global variables
video_path = None
use_webcam = False
alert_triggered = False
alert_expiration = 0
detection_times = []

@app.route('/')
def index():
    """Render the upload page with modern, minimalistic design"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and redirect to streaming page"""
    global video_path, use_webcam, alert_triggered, alert_expiration, detection_times
    use_webcam = False
    alert_triggered = False
    alert_expiration = 0
    detection_times = []
    f = request.files['file']
    if f and f.filename.endswith('.mp4'):
        video_path = f'uploads/{uuid4().hex}.mp4'
        f.save(video_path)
        return redirect('/stream')
    return 'Arquivo inválido. Por favor, faça upload de um vídeo MP4.', 400

@app.route('/webcam')
def webcam():
    """Set up for webcam streaming and redirect to streaming page"""
    global use_webcam, video_path, alert_triggered, alert_expiration, detection_times
    use_webcam = True
    video_path = None
    alert_triggered = False
    alert_expiration = 0
    detection_times = []
    return redirect('/stream')

@app.route('/stream')
def stream():
    """Render the streaming page with video feed and alert system"""
    return render_template('stream.html')

@app.route('/get_alert')
def get_alert():
    """Return the current alert status as JSON"""
    global alert_triggered
    return {'alert': alert_triggered}

@app.route('/video_feed')
def video_feed():
    """Stream video frames with YOLO detection"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    """Generate video frames with YOLO detection and fire/smoke alerts"""
    global alert_triggered, alert_expiration, detection_times, video_path, use_webcam
    
    if use_webcam:
        cap = cv2.VideoCapture(0)  # 0 is the default webcam
    else:
        if video_path is None:
            return
        cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO inference on the frame
        results = model(frame)
        
        conf_threshold = 0.55
        
        # Filter boxes to only include those with confidence >= 0.55
        mask = results[0].boxes.conf >= conf_threshold
        results[0].boxes = results[0].boxes[mask]
        
        # Annotate the frame with detections (boxes and labels) - only high conf now
        annotated_frame = results[0].plot()
        
        # Check for fire or smoke detections with conf >= 0.55
        current_time = time.time()
        has_detection = False
        for box in results[0].boxes:
            cls_id = int(box.cls)
            cls_name = results[0].names[cls_id]
            conf = float(box.conf)
            if cls_name.lower() in ['fire', 'smoke'] and conf >= conf_threshold:
                has_detection = True
                break
        
        if has_detection:
            detection_times.append(current_time)
            # Remove old detections outside 2.5s window
            detection_times = [t for t in detection_times if current_time - t <= 2.5]
        
        # Trigger or extend alert
        if len(detection_times) >= 2:
            alert_triggered = True
            alert_expiration = current_time + 25
        
        if alert_triggered and has_detection:
            alert_expiration = current_time + 25  # Extend to now + 25s on each detection
        
        # Check if alert has expired
        if alert_triggered and current_time > alert_expiration:
            alert_triggered = False
            detection_times = []  # Reset detections after expiration
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()
    # Optionally, delete the video file after processing if not webcam
    if not use_webcam and video_path:
        # os.remove(video_path)
        pass

if __name__ == '__main__':
    app.run(debug=True)