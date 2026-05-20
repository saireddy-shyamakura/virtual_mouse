import cv2
import mediapipe as mp
import pyautogui
import time

# ---------------- SETTINGS ----------------
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

smooth_x = 3
smooth_y = 6
frame_reduction = 80
dead_zone = 4

click_threshold = 0.035
click_delay = 0.3

# ---------------- SCREEN ----------------
screen_w, screen_h = pyautogui.size()

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# ---------------- STATE ----------------
prev_x, prev_y = 0, 0
last_click_time = 0

# ---------------- LOOP ----------------
while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark

            # -------- Fingertip tracking (accurate + stable) --------
            alpha = 0.8
            x_norm = lm[8].x * alpha + lm[6].x * (1 - alpha)
            y_norm = lm[8].y * alpha + lm[6].y * (1 - alpha)

            x = int(x_norm * w)
            y = int(y_norm * h)

            # -------- Limit region --------
            x = max(frame_reduction, min(w - frame_reduction, x))
            y = max(frame_reduction, min(h - frame_reduction, y))

            # -------- Map to screen --------
            screen_x = (x - frame_reduction) * screen_w / (w - 2 * frame_reduction)
            screen_y = (y - frame_reduction) * screen_h / (h - 2 * frame_reduction)

            # -------- Dead zone (remove jitter) --------
            if abs(screen_y - prev_y) < dead_zone:
                screen_y = prev_y

            # -------- Smooth movement --------
            curr_x = prev_x + (screen_x - prev_x) / smooth_x
            curr_y = prev_y + (screen_y - prev_y) / smooth_y

            # -------- Limit sudden jumps --------
            max_step = 80
            dx = curr_x - prev_x
            dy = curr_y - prev_y

            if abs(dx) > max_step:
                curr_x = prev_x + max_step * (dx / abs(dx))

            if abs(dy) > max_step:
                curr_y = prev_y + max_step * (dy / abs(dy))

            # -------- Clamp to screen --------
            curr_x = max(0, min(screen_w - 1, int(curr_x)))
            curr_y = max(0, min(screen_h - 1, int(curr_y)))

            # -------- Move mouse --------
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # -------- CLICK (pinch) --------
            thumb = lm[4]
            index = lm[8]

            distance = ((thumb.x - index.x)**2 + (thumb.y - index.y)**2) ** 0.5
            current_time = time.time()

            if distance < click_threshold and (current_time - last_click_time) > click_delay:
                pyautogui.click()
                last_click_time = current_time

            # -------- Draw pointer --------
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    cv2.imshow("Virtual Mouse Stable", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()