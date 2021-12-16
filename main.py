
import cv2


def main():

    #TODO(shota.nishyama44@gmail.com): frame difference method
    cap = cv2.VideoCapture(0)
    counter = 0
    while(1):
        #capture frameの作成
        if counter == 0:










        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()