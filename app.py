from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import numpy as np
import threading
import base64
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Global variables
camera = None
cap = None
drawing_data = {'points': [], 'color': (0, 0, 0), 'size': 5}
gesture_queue = deque(maxlen=10)

def get_gesture(hand_landmarks):
    """
    Detect hand gestures
    Returns: 'peace', 'thumbs_up', 'thumbs_down', 'open_palm', 'pointing', None
    """
    if not hand_landmarks:
        return None
    
    lm = hand_landmarks.landmark
    
    # Extract key points
    thumb_tip = lm[4]
    index_tip = lm[8]
    middle_tip = lm[12]
    ring_tip = lm[16]
    pinky_tip = lm[20]
    palm_center = lm[9]
    
    # Helper function to check if finger is up
    def finger_up(tip, pip):
        return tip.y < pip.y
    
    # Check fingers up/down
    thumb_up = thumb_tip.x < lm[3].x
    index_up = finger_up(index_tip, lm[6])
    middle_up = finger_up(middle_tip, lm[10])
    ring_up = finger_up(ring_tip, lm[14])
    pinky_up = finger_up(pinky_tip, lm[18])
    
    fingers_up = [index_up, middle_up, ring_up, pinky_up]
    count = sum(fingers_up)
    
    # Peace sign: index and middle up
    if index_up and middle_up and not ring_up and not pinky_up:
        return 'peace'
    
    # Thumbs up: only thumb up, hand vertical
    if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        if abs(lm[0].x - palm_center.x) < 0.1:
            return 'thumbs_up'
    
    # Thumbs down: thumb down
    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return 'thumbs_down'
    
    # Open palm: all fingers up
    if all(fingers_up) and thumb_up:
        return 'open_palm'
    
    # Pointing: only index finger up
    if index_up and not middle_up and not ring_up and not pinky_up:
        return 'pointing'
    
    return None

def camera_thread():
    """Capture video and emit frames via WebSocket"""
    global cap
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip for selfie view
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        gesture = None
        index_finger_pos = None
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                # Get gesture
                gesture = get_gesture(hand_landmarks)
                
                # Get index finger position
                index_tip = hand_landmarks.landmark[8]
                index_finger_pos = {
                    'x': int(index_tip.x * w),
                    'y': int(index_tip.y * h)
                }
                
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).tobytes()
        
        # Emit frame and hand data
        socketio.emit('video_frame', {
            'frame': frame_base64.decode('utf-8'),
            'gesture': gesture,
            'index_pos': index_finger_pos
        })

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('drawing_data')
def handle_drawing(data):
    """Receive drawing coordinates from client"""
    global drawing_data
    drawing_data = data

@socketio.on('start_camera')
def handle_start_camera():
    """Start camera thread"""
    thread = threading.Thread(target=camera_thread, daemon=True)
    thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
