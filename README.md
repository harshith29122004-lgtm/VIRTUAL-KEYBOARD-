<h1 align="center">⌨️ Virtual Keyboard</h1>

<p align="center">
  <b>Touchless typing using hand tracking and computer vision</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green" />
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange" />
</p>

## 📌 About

Virtual Keyboard is a Python application that lets a user type using hand movements in front of a webcam, without a physical keyboard.

The application tracks one hand, uses the index fingertip to move over on-screen keys, and detects a pinch between the thumb and index finger to select a key. It includes letter keys, Space, and Backspace.

## ✨ Features

- Webcam-based hand tracking.
- On-screen QWERTY keyboard.
- Index-finger movement to highlight keys.
- Thumb-and-index pinch gesture to select a key.
- Space and Backspace support.
- Live typed-text preview.

## 🛠️ Built With

- **Python** — application logic.
- **OpenCV** — webcam input and drawing the interface.
- **MediaPipe** — hand landmark detection and tracking.

## 📁 Project Structure

```text
Virtual-Keyboard/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    └── screenshots/
        └── .gitkeep
```

## ⚙️ Setup and Run

### 1. Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/Virtual-Keyboard.git
cd Virtual-Keyboard
```

### 2. Create and activate a virtual environment (recommended)

**Windows:**
```bash
py -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
python main.py
```

Allow the application to access your webcam. Move your index finger over a key and pinch your thumb and index finger together to select it. Press **Q** to quit.

## 💻 Requirements

- Python 3.10–3.12 recommended.
- A working webcam.
- Windows, macOS, or Linux.
- Webcam permission enabled for your terminal or IDE.

## 🧭 How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe detects hand landmarks in each frame.
3. The application follows the index fingertip and checks which key it is over.
4. When the thumb and index fingertip come close together, the hovered key is selected.
5. The selected character is displayed in the typed-text preview.

## 🔧 Troubleshooting

- **Camera not opening:** Close other apps that may be using the webcam and check camera permissions.
- **Dependency installation fails:** Use Python 3.10, 3.11, or 3.12 in a fresh virtual environment, then reinstall `requirements.txt`.
- **Hand tracking is unstable:** Improve lighting, keep your hand inside the camera view, and avoid covering your fingertips.

## 👨‍💻 Developer

**Harshith D S**  
Information Science Engineering Graduate

- Email: harshith29122004@gmail.com
- LinkedIn: https://www.linkedin.com/in/harshith-ds-7a786030b

---

<p align="center">Built with Python, OpenCV and MediaPipe 💻</p>
