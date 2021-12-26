#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import gc
from typing import List
import os
import pathlib
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

from face_detector_deep import FaceDetector
from face_indentification import FaceFeatureExtractor

DEFAULT_DIR = './images/Authenticated_image'


class Register:

    def __init__(self, face_dir=DEFAULT_DIR):

        self.faces_directory_path = face_dir

    def adjust_extension(self) -> None:

        files = [filename for filename in os.listdir(self.faces_directory_path) if not filename.startswith('.')]
        extension = 'jpg'
        for file in files:
            file_suffix = pathlib.PurePath(file).suffix
            if file_suffix == 'jpeg' or 'JPG':
                file_name = pathlib.PurePath(file).stem
                jpg_file = file_name + extension
                shutil.move(file, jpg_file)
            if file_suffix == 'png' or 'PNG':
                file_name = pathlib.PurePath(file).stem
                im = Image.open(file)
                im = im.convert("RGB")
                jpg_file = file_name + extension
                im.save(jpg_file)

    def search_face_files(self) -> List[str]:

        if not os.path.isdir(self.faces_directory_path):
            print(f'directory is not found. {self.faces_directory_path}')
            sys.exit(-1)
        # get file name, other than hidden file. example for .DS_STORE
        files = [filename for filename in os.listdir(self.faces_directory_path) if not filename.startswith('.')]
        return files

    def save_feature_vector(self, files: List[str], save_path: str) -> None:

        for file in files:

            img = cv2.imread(file)
            detector = FaceDetector(img)
            cropped_face_img = detector.detecte_face()
            del detector
            gc.collect()

            # face feature extraction
            feature_extractor = FaceFeatureExtractor(cropped_face_img)
            face_embedding_vector = feature_extractor.feature_extraction()
            del feature_extractor
            gc.collect()

            file_name = pathlib.PurePath(file).stem
            file_name = file_name + '.npy'
            save_path = os.path.join(save_path, file_name)
            np.save('save_path', face_embedding_vector)