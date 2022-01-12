#  Copyright (c) 2021 by Shota NISHIYAMA
import argparse
import gc
import os
import sys

import cv2

from dotenv import load_dotenv
from akaze_feature_matching import get_face_similarity
from face_detector import HaarFaceDetector
from face_detector_deep import FaceDetector
from face_indentification import FaceIdentificator
from face_indentification import FaceFeatureExtractor
from sender import LineSender
from util import load_yaml


def main():
    # argument
    parser = argparse.ArgumentParser(description='surveillance-came args')
    parser.add_argument('--deep', action='store_true')
    args = parser.parse_args()
    is_deep = args.deep
    # config setting
    config_yaml_file_path = './config.yaml'
    config = load_yaml(config_yaml_file_path)
    threshold = config['threshold_of_frame_difference_method']
    mask_threshold = config['threshold_of_number_of_white_pixel']
    threshold_of_degree_of_similarity = config['threshold_of_degree_of_similarity']
    degree_of_similarity = 0
    # load env
    load_dotenv(verbose=True)
    LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    LINE_USER_ID = os.getenv("LINE_USER_ID")

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
        number_of_white_pixel = mask.sum()

        if number_of_white_pixel > mask_threshold:
            cv2.imshow("curr_img", curr_img)
            # Deep
            if is_deep:
                # face detection
                print('face detecting...')
                detector = FaceDetector(curr_img)
                cropped_face_img = detector.detecte_face()
                detector.show()
                del detector
                gc.collect()
                # feature extraction
                print('feature extraction...')
                feature_extractor = FaceFeatureExtractor(cropped_face_img)
                face_embedding_vector1 = feature_extractor.feature_extraction()
                del feature_extractor
                gc.collect()
                # face identficate between 2 images.
                print('face identification...')
                face_identificator = FaceIdentificator(face_embedding_vector1, face_embedding_vector1)
                degree_of_similarity = face_identificator.identfy()
                # print(f'degree of similarity is {degree_of_similarity:.4} between {file_name1} and {file_name2}.')
            else:
                '''
                TODO Shoma Kato: Develop classical detection, recognition and identification algorithm.
                '''
                haar_detector = HaarFaceDetector('./models/haarcascade_frontalface_default.xml')
                cropped_face_img = haar_detector.getFaceImage(curr_img)
                if cropped_face_img is not None:
                    # TODO Template needs to be specified.
                    degree_of_similarity = get_face_similarity(cropped_face_img, "")
                
                pass
            print(degree_of_similarity)
            if degree_of_similarity < threshold_of_degree_of_similarity:
                msg = '不審者発見'
                # line_sender = LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)
                # line_sender.send_to_line(msg)

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