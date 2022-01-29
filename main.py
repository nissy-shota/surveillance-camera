#  Copyright (c) 2021 by Shota NISHIYAMA
import argparse
from distutils.command import register
import gc
from multiprocessing import connection, managers
import os
import sys

import cv2

from dotenv import load_dotenv
from akaze_feature_matching import get_face_similarity
from face_detector import HaarFaceDetector
from face_detector_deep import FaceDetector
from face_indentification import FaceIdentificator
from face_indentification import FaceFeatureExtractor
from manager import FaceIdentificationManager
from sender import LineSender
from util import load_yaml
from register import FaceRegister

def regist():
    register = FaceRegister()
    files = register.search_face_files()
    register.save_feature_vector(files, "./images/Face_Vectors")

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
    threshold_of_degree_of_similarity_with_akaze = config['threshold_of_degree_of_similarity_with_akaze']
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
    frame_counter = 0
    already_executed = True
    while True:

        if counter == 0:
            _, prev_img = cap.read()
            prev_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)
            back = cv2.imread("./images/back.jpg", cv2.IMREAD_GRAYSCALE)
            height, width, channels = prev_img.shape[:3]
            counter += 1
            continue

        _, curr_img = cap.read()
        curr_gray = cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY)
        # create mask
        mask = cv2.absdiff(curr_gray, back)
        cv2.rectangle(mask, (0, 0), (int(width/3), height), 0, thickness=-1, lineType=cv2.LINE_AA, shift=0)
        cv2.rectangle(mask, (int(width/3)*2, 0), (width, height), 0, thickness=-1, lineType=cv2.LINE_AA, shift=0)
        mask[mask < threshold] = 0
        mask[mask >= threshold] = 255
        # cv2.imshow("mask", mask)
        number_of_white_pixel = mask.sum()
        
        
        if already_executed == True and number_of_white_pixel < 5000000:
            already_executed = False
            frame_counter = 0
            print("Reset")
        
        if number_of_white_pixel > mask_threshold:
            frame_counter += 1
        
        if number_of_white_pixel > mask_threshold and already_executed == False and frame_counter > 60:
            
            # Deep
            if is_deep:
                # face detection
                print('face detecting...')
                detector = FaceDetector(curr_img)
                cropped_face_img = detector.detecte_face()
                # No face was detected.
                if cropped_face_img is None:
                    print("None")
                    continue
                
                # detector.show()
                del detector
                gc.collect()
                # feature extraction
                print('feature extraction...')
                feature_extractor = FaceFeatureExtractor(cropped_face_img)
                face_embedding_vector1 = feature_extractor.feature_extraction()
                del feature_extractor
                gc.collect()
                # face identficate between 2 images.
                manager = FaceIdentificationManager(face_embedding_vector1)
                degree_of_similarity = manager.identification()
                
                if degree_of_similarity < threshold_of_degree_of_similarity:
                    msg = '不審者発見'
                    # line_sender = LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)
                    # line_sender.send_to_line(msg)
                    print(msg)
                
                already_executed = True
                cv2.imshow("curr", curr_img)
            else:
                '''
                TODO Shoma Kato: Develop classical detection, recognition and identification algorithm.
                '''
                haar_detector = HaarFaceDetector('./models/haarcascade_frontalface_default.xml')
                cropped_face_img = haar_detector.getFaceImage(curr_img)
                if cropped_face_img is not None:
                    # TODO Template needs to be specified.
                    degree_of_similarity = get_face_similarity(cropped_face_img, "images/akaze_template/*")
                
                if degree_of_similarity == 0 or degree_of_similarity == -1:
                    continue
                
                if cropped_face_img is None:
                    continue
                
                print(degree_of_similarity)
                if degree_of_similarity > threshold_of_degree_of_similarity_with_akaze:
                    msg = '不審者発見'

                    print(msg)
                # line_sender = LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)
                # line_sender.send_to_line(msg)
                already_executed = True
                cv2.imshow("curr", curr_img)

        prev_gray = curr_gray
        del curr_gray
        gc.collect()

        counter += 1
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    # regist()
    main()