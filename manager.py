#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import torch

from face_indentification import FaceIdentificator


class FaceIdentificationManager:

    def __init__(self, face_embedding_vector: np.array, face_vector_dir='./images/Face_Vectors'):
        self.face_embedding_vector = face_embedding_vector
        self.face_vector_dir = face_vector_dir

    def get_registered_embedding_vector_files(self) -> List[np.array]:

        face_vector_files = [filename for filename in os.listdir(self.face_vector_dir) if not filename.startswith('.')]

        return face_vector_files

    def identification(self):
        
        degree_of_similarity_list = []
        face_vector_files = self.get_registered_embedding_vector_files()
        for face_vector_file in face_vector_files:

            face_vector_path = os.path.join(self.face_vector_dir, face_vector_file)
            try:
                registered_embedding_vector = np.load(face_vector_path)
            except IOError as e:
                print('File is not found.')
                continue
            except ValueError as e:
                print('The file contains an object array, but allow_pickle=False given.')
                continue
            # numpy to tensor
            registered_embedding_vector = torch.from_numpy(registered_embedding_vector.astype(np.float32)).clone()
            
            face_identificator = FaceIdentificator(self.face_embedding_vector, registered_embedding_vector)
            degree_of_similarity = face_identificator.identfy()
            degree_of_similarity_list.append(degree_of_similarity)
            
        return max(degree_of_similarity_list)


