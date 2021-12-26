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


class FaceRegister:

    '''
    Register class.
    This class is for registering faces that do not need to be notified to the line.
    '''

    def __init__(self, face_dir=DEFAULT_DIR):

        self.faces_directory_path = face_dir

    def align_extension(self) -> None:
        '''
        Align the extension format to jpg.
        For example, jpeg, JPG ...
        If the file contains png or png, convert it to jpg and save it.
        Returns: None

        '''

        files = [filename for filename in os.listdir(self.faces_directory_path) if not filename.startswith('.')]
        extension = '.jpg'
        for file in files:
            file_suffix = pathlib.PurePath(file).suffix

            if file_suffix == ('.jpeg' or '.JPG'):
                file_name = pathlib.PurePath(file).stem
                jpg_file = file_name + extension
                save_path = os.path.join(self.faces_directory_path, jpg_file)
                original_path = os.path.join(self.faces_directory_path, file)
                shutil.move(original_path, save_path)

            if file_suffix == ('.png' or '.PNG'):
                file_name = pathlib.PurePath(file).stem
                im = Image.open(file)
                im = im.convert("RGB")
                jpg_file = file_name + extension
                save_path = os.path.join(self.faces_directory_path, jpg_file)
                im.save(save_path)

    def search_face_files(self) -> List[str]:
        '''
        return all of files in the directory
        Returns: files

        '''

        if not os.path.isdir(self.faces_directory_path):
            print(f'directory is not found. {self.faces_directory_path}')
            sys.exit(-1)
        # get file name, other than hidden file. example for .DS_STORE
        files = [filename for filename in os.listdir(self.faces_directory_path) if not filename.startswith('.')]
        return files

    def save_feature_vector(self, files: List[str], save_path: str) -> None:

        '''
        Convert faces into features and store them.
        Args:
            files: get search_face_files()
            save_path: save path

        Returns: None

        '''

        for file in files:
            file_path = os.path.join(self.faces_directory_path, file)
            img = cv2.imread(file_path)
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            detector = FaceDetector(image)
            cropped_face_img = detector.detecte_face()
            del detector
            gc.collect()

            if cropped_face_img is None:
                continue


            # face feature extraction
            feature_extractor = FaceFeatureExtractor(cropped_face_img)
            face_embedding_vector = feature_extractor.feature_extraction()
            face_embedding_vector = face_embedding_vector.squeeze().to('cpu').detach().numpy().copy()
            del feature_extractor
            gc.collect()

            file_name = pathlib.PurePath(file).stem
            file_name = file_name + '.npy'
            np.save(os.path.join(save_path, file_name), face_embedding_vector)