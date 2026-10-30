# Virtual Keyboard

A touchless virtual keyboard built with **Python, OpenCV, and MediaPipe**. The application uses a webcam to track one hand and lets you select on-screen keys with finger gestures.

## Features

- Webcam-based hand landmark tracking.
- On-screen QWERTY keyboard.
- Index-finger movement to hover over keys.
- Thumb-and-index-finger pinch gesture to select a key.
- Letter, Space, and Backspace support.
- Live typed-text preview.

## Technology

- Python 3.10–3.12
- OpenCV — webcam capture and interface rendering
- MediaPipe — hand landmark detection and tracking

## Requirements

- Python 3.10, 3.11, or 3.12
- A working webcam
- Webcam permission enabled for your terminal or IDE

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/harshith29122004-lgtm/VIRTUAL-KEYBOARD-.git
   cd VIRTUAL-KEYBOARD-
   ```

2. Create and activate a virtual environment.

   **Windows**
   ```bash
   py -3.10 -m venv venv
   venv\\Scripts\\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python main.py
   ```

Allow webcam access when prompted. Move your index fingertip over a key and bring your thumb and index finger together to select it. Press **Q** to quit.

## Troubleshooting

- **Camera does not open:** Close other applications using the webcam and check operating-system camera permissions.
- **Dependency installation fails:** Use Python 3.10–3.12 in a fresh virtual environment, then reinstall the requirements.
- **Tracking is unstable:** Improve lighting, keep your hand within the camera frame, and avoid covering your fingertips.

## Author

**Harshith D S** · [LinkedIn](https://www.linkedin.com/in/harshith-ds-7a786030b/)
