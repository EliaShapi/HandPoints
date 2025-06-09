import cv2
import numpy as np
import pygame

def show_start_menu():

    pygame.mixer.init()
    start_sound = pygame.mixer.Sound("assets/start_sound.wav")

    while True:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # white background

        cv2.putText(frame, 'Welcome to HandPoints', (120, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv2.putText(frame, 'Press S to Start', (170, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, 'or Q to quit', (190, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        frame = cv2.copyMakeBorder(frame, 40, 40, 40, 40, borderType=cv2.BORDER_CONSTANT, value=(200,200,200))
        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, borderType=cv2.BORDER_CONSTANT, value=(100,100,100))
        cv2.imshow('Start Menu', frame)

        key = cv2.waitKey(30) & 0xFF  # 30 millasecond delay
        if key == ord('s'):
            start_sound.play()
            cv2.destroyWindow('Start Menu')
            break
        '''elif key == 27 or ord('q'):
            cv2.destroyAllWindows()
            exit()'''