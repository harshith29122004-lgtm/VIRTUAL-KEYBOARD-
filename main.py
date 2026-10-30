"""
Virtual Keyboard - Touchless typing with hand tracking.

Controls:
- Move your index finger over a key to highlight it.
- Pinch your thumb and index finger together while hovering over a key to press it.
- Press Q to quit.

Tested design target: Python 3.10-3.12, OpenCV, MediaPipe.
"""

import time
import cv2
import mediapipe as mp

WINDOW_NAME = "Virtual Keyboard - Hand Tracking"

KEY_ROWS = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM") + ["SPACE", "BACK"],
]

BACKGROUND = (28, 30, 38)
KEY_COLOR = (55, 61, 75)
HOVER_COLOR = (80, 145, 220)
TEXT_COLOR = (245, 247, 250)
ACCENT = (80, 210, 160)


def build_key_rectangles(frame_width, frame_height):
    """Return key rectangles positioned in the lower part of the camera frame."""
    margin_x = 35
    gap = 7
    key_height = max(38, int(frame_height * 0.075))
    start_y = int(frame_height * 0.53)
    usable_width = frame_width - 2 * margin_x
    rectangles = []

    for row_index, row in enumerate(KEY_ROWS):
        row_y = start_y + row_index * (key_height + gap)
        # Special keys take more horizontal space.
        weights = [2.2 if key in ("SPACE", "BACK") else 1.0 for key in row]
        total_weight = sum(weights)
        unit_width = (usable_width - gap * (len(row) - 1)) / total_weight
        x = margin_x
        for key, weight in zip(row, weights):
            width = int(unit_width * weight)
            rectangles.append((key, (int(x), row_y, int(x + width), row_y + key_height)))
            x += width + gap
    return rectangles


def point_in_rect(point, rect):
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2


def draw_keyboard(frame, rectangles, hovered_key, typed_text):
    height, width = frame.shape[:2]

    # Translucent keyboard panel.
    overlay = frame.copy()
    panel_top = int(height * 0.49)
    cv2.rectangle(overlay, (18, panel_top), (width - 18, height - 15), BACKGROUND, -1)
    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

    cv2.putText(frame, "VIRTUAL KEYBOARD", (32, panel_top - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, ACCENT, 2, cv2.LINE_AA)

    for key, (x1, y1, x2, y2) in rectangles:
        color = HOVER_COLOR if key == hovered_key else KEY_COLOR
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1, cv2.LINE_AA)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (115, 125, 145), 1, cv2.LINE_AA)
        label = "SPACE" if key == "SPACE" else ("⌫" if key == "BACK" else key)
        font_scale = 0.48 if key in ("SPACE", "BACK") else 0.62
        thickness = 1 if key in ("SPACE", "BACK") else 2
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        tx = x1 + (x2 - x1 - text_size[0]) // 2
        ty = y1 + (y2 - y1 + text_size[1]) // 2
        cv2.putText(frame, label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, TEXT_COLOR, thickness, cv2.LINE_AA)

    # Typed text preview.
    preview = typed_text[-42:] if typed_text else "Your typed text will appear here..."
    cv2.putText(frame, "TYPED TEXT:", (32, 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.58, ACCENT, 2, cv2.LINE_AA)
    cv2.putText(frame, preview, (32, 75), cv2.FONT_HERSHEY_SIMPLEX,
                0.72, TEXT_COLOR, 2, cv2.LINE_AA)
    cv2.putText(frame, "Move index finger to a key | Pinch thumb + index to select | Q to quit",
                (24, height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.42,
                (220, 220, 220), 1, cv2.LINE_AA)


def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError(
            "Could not open the webcam. Check camera permissions or try another camera index."
        )

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    typed_text = ""
    last_press_time = 0.0
    pinch_was_active = False
    press_cooldown = 0.45

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.65,
            min_tracking_confidence=0.6,
        ) as hands:
            while True:
                success, frame = camera.read()
                if not success:
                    print("Unable to read from webcam.")
                    break

                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]
                rectangles = build_key_rectangles(width, height)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                hovered_key = None
                pinch_active = False
                finger_point = None

                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    index_tip = hand_landmarks.landmark[8]
                    thumb_tip = hand_landmarks.landmark[4]
                    finger_point = (int(index_tip.x * width), int(index_tip.y * height))

                    pinch_distance = (
                        (index_tip.x - thumb_tip.x) ** 2
                        + (index_tip.y - thumb_tip.y) ** 2
                    ) ** 0.5
                    pinch_active = pinch_distance < 0.045

                    for key, rect in rectangles:
                        if point_in_rect(finger_point, rect):
                            hovered_key = key
                            break

                    cv2.circle(frame, finger_point, 10, ACCENT, -1, cv2.LINE_AA)
                    cv2.circle(frame, finger_point, 17, (255, 255, 255), 2, cv2.LINE_AA)

                    now = time.time()
                    if (
                        hovered_key
                        and pinch_active
                        and not pinch_was_active
                        and now - last_press_time >= press_cooldown
                    ):
                        if hovered_key == "SPACE":
                            typed_text += " "
                        elif hovered_key == "BACK":
                            typed_text = typed_text[:-1]
                        else:
                            typed_text += hovered_key
                        last_press_time = now

                    pinch_was_active = pinch_active
                else:
                    pinch_was_active = False

                draw_keyboard(frame, rectangles, hovered_key, typed_text)

                status = "PINCH: SELECT" if pinch_active else "TRACKING: MOVE TO A KEY"
                cv2.putText(frame, status, (width - 300, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                            ACCENT if pinch_active else TEXT_COLOR, 1, cv2.LINE_AA)

                cv2.imshow(WINDOW_NAME, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        print("Tip: install the dependencies and make sure your webcam is available.")
