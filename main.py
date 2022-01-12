#  Copyright (c) 2021 by Shota NISHIYAMA

import cv2
import gc
from util import load_yaml


def main():

    # config setting
    config_yaml_file_path = './config.yaml'
    config = load_yaml(config_yaml_file_path)
    threshold = config['threshold_of_frame_difference_method']

    #TODO(shota.nishyama44@gmail.com): frame difference method
    # real time capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    counter = 0
    while True:

        if counter == 0:
            _, prev_img = cap.read()
            prev_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)
            counter += 1
            continue

        _, curr_img = cap.read()
        curr_gray = cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY)
        # create mask
        mask = cv2.absdiff(curr_gray, prev_gray)
        mask[mask < threshold] = 0
        mask[mask >= threshold] = 255
        
        cv2.imshow("Mask", mask)

        prev_gray = curr_gray
        del curr_gray
        gc.collect()

        counter += 1
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()