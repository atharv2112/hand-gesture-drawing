# ✋ Hand Gesture Drawing

A real-time web-based application that lets you draw on a canvas using hand gestures detected through your webcam!

## Features

✨ **Real-Time Hand Tracking** - Uses MediaPipe for accurate hand detection  
🎨 **Canvas Drawing** - Draw by pointing your index finger  
🌈 **Multiple Colors** - 6 vibrant colors to choose from  
📏 **Adjustable Brush Size** - From 1px to 30px  
♻️ **Undo & Clear** - Undo strokes or clear the entire canvas  
👆 **Gesture Controls** - Use hand gestures to control tools:
  - ✌️ Peace Sign → Cycle Colors
  - 👍 Thumbs Up → Increase Brush Size
  - 👎 Thumbs Down → Decrease Brush Size
  - ✋ Open Palm → Clear Canvas

## Tech Stack

**Backend:**
- Flask (Web Framework)
- Flask-SocketIO (WebSocket Communication)
- MediaPipe (Hand Detection)
- OpenCV (Image Processing)

**Frontend:**
- HTML5 Canvas
- JavaScript
- Socket.IO Client

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/atharv2112/hand-gesture-drawing.git
cd hand-gesture-drawing
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the server:**
```bash
python app.py
```

2. **Open your browser:**
Navigate to `http://localhost:5000`

3. **Allow webcam access** when prompted

4. **Start drawing:**
- Point your index finger to draw
- Use gestures to control tools
- Colors available: Black, Red, Green, Blue, Yellow, Magenta

## Hand Gestures Guide

| Gesture | Action | How to Do |
|---------|--------|-----------|
| ✌️ Peace Sign | Change Color | Index & middle fingers up |
| 👍 Thumbs Up | Increase Brush Size | Thumb pointing up |
| 👎 Thumbs Down | Decrease Brush Size | Thumb pointing down |
| ✋ Open Palm | Clear Canvas | All fingers extended |
| ☝️ Pointing | Draw Mode | Only index finger up |

## Project Structure

```
hand-gesture-drawing/
├── app.py                   # Flask backend with hand tracking
├── templates/
│   └── index.html          # Web interface with canvas
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works

### Backend (app.py)
1. Captures video from webcam using OpenCV
2. Uses MediaPipe to detect hand landmarks
3. Recognizes hand gestures
4. Extracts index finger coordinates
5. Streams video frames & hand data to frontend via WebSocket

### Frontend (index.html)
1. Displays live video feed
2. Shows detected gestures
3. Draws on canvas based on index finger position
4. Handles color selection & brush size
5. Manages undo & clear functionality

## Tips for Best Performance

✅ Good lighting - Ensures accurate hand detection  
✅ Clear background - Single color background works best  
✅ Stable hand - Smooth movements for better drawing  
✅ Close-up view - Position hand clearly in frame  
✅ Warm up - Let the model initialize (first few seconds)

## Troubleshooting

**Camera not working?**
- Check browser permissions for webcam
- Ensure no other app is using the camera
- Try a different browser

**Hand not detected?**
- Increase lighting
- Move hand closer to camera
- Try different angles

**Shaky drawing?**
- Slow down your hand movements
- Improve lighting conditions
- Ensure stable hand posture

## Future Enhancements

- [ ] Multiple hand support
- [ ] Eraser tool
- [ ] Color picker
- [ ] Shape recognition (circle, square, etc.)
- [ ] Save drawings as image
- [ ] Drawing effects (blur, glow, etc.)
- [ ] Mobile app version

## Performance Notes

- **Resolution**: 640x480 (adjustable in code)
- **FPS**: ~30 (depends on system)
- **Latency**: Minimal WebSocket communication
- **Browser Compatibility**: Chrome, Firefox, Edge, Safari (recent versions)

## Customization

### Change detection confidence:
Edit `app.py` line 33-37:
```python
hands = mp_hands.Hands(
    min_detection_confidence=0.7,  # Increase for stricter detection
    min_tracking_confidence=0.5    # Increase for stable tracking
)
```

### Adjust canvas size:
Edit `templates/index.html` line 240:
```javascript
canvas.width = rect.width - 40;
canvas.height = Math.min(canvas.width, 500);  // Change 500
```

### Add more colors:
Edit `templates/index.html` color-grid section and add:
```html
<button class="color-btn custom-btn" data-color="R,G,B">Label</button>
```

## License

MIT License - Feel free to use, modify, and distribute!

## Author

Created by [@atharv2112](https://github.com/atharv2112)

## Support

For issues, questions, or suggestions:
- Open a GitHub Issue
- Check existing issues for solutions
- Share your improvements via Pull Requests

---

**Enjoy creating art with your hands! 🎨✨**
