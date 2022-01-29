from tkinter.messagebox import NO
import cv2

def save():
    # real time capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    counter = 0
    while True:
        _, curr_img = cap.read()
        if curr_img is not None and counter >= 30:
            cv2.imwrite("./images/back.jpg", curr_img)
            return

        counter += 1

if __name__ == "__main__":
    save()
