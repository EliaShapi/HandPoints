import cv2
import mediapipe as mp
import pyautogui
import random
import math
import pygame
import time

def show_special_effect(frame, x, y, elapsed_time):

    if elapsed_time < 3:
        # אפקט 1 - זוהר סביב הפרס
        glow_color = (0, 255, 255)
        glow_thickness = 2
        max_glow_radius = 40
        glow_radius = int((math.sin(elapsed_time * 10) + 1) / 2 * max_glow_radius) + 10
        cv2.circle(frame, (x, y), glow_radius, glow_color, glow_thickness)



    elif elapsed_time < 6:  # 1 שניה + 2 שניות = 3 שניות

        # אפקט 2 - כוכבים בכל המסך

        height, width, _ = frame.shape

        for _ in range(20):
            star_x = random.randint(0, width - 1)

            star_y = random.randint(0, height - 1)

            cv2.circle(frame, (star_x, star_y), 3, (0, 255, 255), -1)


    else:
        # מעבר לאפקט הבא או סיום האפקטים
        pass


def run_game():
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    screen_width, screen_height = pyautogui.size()

    frame_border = 50
    frame_width, frame_height = 640, 480
    prize_x = random.randint(frame_border, frame_width - frame_border)
    prize_y = random.randint(frame_border, frame_height - frame_border - 100)

    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("assets/click.wav")
    bonus_sound = pygame.mixer.Sound("assets/bonus.wav")
    victory_sound = pygame.mixer.Sound("assets/victory.wav")
    pygame.mixer.music.load("assets/background_music.mp3")
    pygame.mixer.music.play(-1)

    angle1 = 0
    angle2 = 0
    radius1 = 20
    radius2 = 15
    grow = True
    score = 0
    last_face_score = -1  # כדי למנוע חזרתיות
    face_display_until = 0  # זמן עד מתי להציג את הפנים

    max_time = 15
    start_time = time.time()

    effect_frame_count = 0  # ספירת פריימים לאפקטים

    def rotate_point(x, y, cx, cy, angle_rad):
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)
        dx = x - cx
        dy = y - cy
        rotated_x = cx + cos_theta * dx - sin_theta * dy
        rotated_y = cy + sin_theta * dx + cos_theta * dy
        return int(rotated_x), int(rotated_y)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        cv2.circle(frame, (prize_x, prize_y), 20, (0, 255, 0), -1)

        angle1 += 0.05
        points1 = []
        for i in range(4):
            a = angle1 + i * (math.pi / 2)
            x, y = rotate_point(prize_x + radius1, prize_y, prize_x, prize_y, a)
            points1.append((x, y))
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
        for i in range(4):
            cv2.line(frame, points1[i], points1[(i + 1) % 4], (255, 0, 0), 2)

        angle2 -= 0.02
        if grow:
            radius2 += 0.4
            if radius2 >= 20:
                grow = False
        else:
            radius2 -= 0.4
            if radius2 <= 10:
                grow = True
        points2 = []
        for i in range(4):
            a = angle2 + i * (math.pi / 2)
            x, y = rotate_point(prize_x + radius2, prize_y, prize_x, prize_y, a)
            points2.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 165, 255), -1)
        for i in range(4):
            cv2.line(frame, points2[i], points2[(i + 1) % 4], (0, 165, 255), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS,
                                             landmark_drawing_spec=drawing_utils.DrawingSpec(color=(0, 255, 255),
                                                                                             thickness=2,
                                                                                             circle_radius=3),
                                             connection_drawing_spec=drawing_utils.DrawingSpec(color=(0, 128, 255),
                                                                                               thickness=2,
                                                                                               circle_radius=2))

                for id, landmark in enumerate(hand.landmark):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:
                        cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
                        cv2.circle(frame, (x, y), 7, (50, 150, 150), -1)
                        if abs(x - prize_x) < 20 and abs(y - prize_y) < 20:
                            prize_x = random.randint(frame_border, frame_width - frame_border)
                            prize_y = random.randint(frame_border, frame_height - frame_border - 100)
                            score += 1
                            click_sound.play()
                            start_time += 1

        # הצגת נקודות פנים כל 5 נקודות חדשות
        if score > 0 and score % 5 == 0 and score != last_face_score:
            bonus_sound.play()
            face_display_until = time.time() + 2  # show face mesh for 2 seconds
            last_face_score = score

        # Draw face mesh if inside display window
        if time.time() < face_display_until:
            face_results = face_mesh.process(rgb_frame)
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    drawing_utils.draw_landmarks(
                        frame,
                        face_landmarks,
                        mp.solutions.face_mesh.FACEMESH_TESSELATION,
                        drawing_utils.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                        drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=1)
                    )

        # אפקטים מיוחדים סביב הפרס בכל פעם שהניקוד כפולה של 5
        if score % 5 == 0 and score != 0:
            effect_frame_count += 1
            show_special_effect(frame, prize_x, prize_y, effect_frame_count)
        else:
            effect_frame_count = 0

        # טיימר
        elapsed = time.time() - start_time
        remaining = max_time - elapsed
        if remaining <= 0:
            break

        bar_x, bar_y = 50, 440
        bar_width, bar_height = 540, 20
        fill_width = int((remaining / max_time) * bar_width)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (169, 169, 169), -1)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), (0, 255, 0), -1)
        cv2.putText(frame, f"Time: {int(remaining)}s", (bar_x + 10, bar_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.putText(frame, f'Score: {score}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

        cv2.imshow('HandPoints', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    pygame.mixer.music.stop()
    victory_sound.play()
    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()
    return score
