import cv2
import numpy as np

def show_end_screen(score):
    while True:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # מסך לבן

        cv2.putText(frame, f'Game Over! Your score: {score}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(frame, 'Press Q to Quit or R to Restart', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        frame = cv2.copyMakeBorder(frame, 40, 40, 40, 40, borderType=cv2.BORDER_CONSTANT, value=(200, 200, 200))
        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, borderType=cv2.BORDER_CONSTANT, value=(100, 100, 100))
        cv2.imshow('End Screen', frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit()
        elif key == ord('r'):
            cv2.destroyWindow('End Screen')
            return
