#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import numpy as np
from torchtyping import TensorType

from facenet_pytorch import InceptionResnetV1


class FaceFeatureExtractor:
    '''
    face feature extraction class
    Attributes:
        detected_face  (TensorType): cropped image from face detector

    Examples:
        >>> feature_extractor = FaceFeatureExtractor(cropped_face_img1)
        >>> face_embedding_vector1 = feature_extractor.feature_extraction()
    '''

    def __init__(self, detected_face):

        self.detected_face = detected_face

    def feature_extraction(self) -> TensorType:
        '''
        feature extraction, embedding vector shape is torch.Size([1, 512])
        Returns:embedding_vector

        '''

        resnet = InceptionResnetV1(pretrained='vggface2').eval()
        embedding_vector = resnet(self.detected_face.unsqueeze(0))

        return embedding_vector


class FaceIdentificator:
    '''
    face identification class
    Attributes:
        embedding_vector1  (TensorType): embedding vector from feature extraction
        embedding_vector2  (TensorType): embedding vector from feature extraction
        degree_of_similarity (np.array): degree of similarity

    Examples:
        >>> face_identificator = FaceIdentificator(face_embedding_vector1, face_embedding_vector2)
        >>> degree_of_similarity = face_identificator.identfy()
    '''

    def __init__(self, embedding_vector1: TensorType, embedding_vector2: TensorType, TH = 0.7):

        self.embedding_vector1 = embedding_vector1
        self.embedding_vector2 = embedding_vector2
        self.TH = TH

    def __cos_similarity(self, embedding_vector1: np.ndarray, embedding_vector2: np.ndarray) -> np.ndarray:
        '''
        Args:
            embedding_vector1: np.ndarray
            embedding_vector2: np.ndarray
        Returns: cosine simillarity
        '''

        return np.dot(embedding_vector1, embedding_vector2) / (np.linalg.norm(embedding_vector1) * np.linalg.norm(embedding_vector2))

    def __preprocess(self, embedding_vector1: TensorType, embedding_vector2: TensorType):
        '''

        Args:
            embedding_vector1: TensorType
            embedding_vector2: TensorType

        Returns:
            embedding_vector1: np.ndarray
            embedding_vector2: np.ndarray
        '''

        embedding_vector1 = embedding_vector1.squeeze().to('cpu').detach().numpy().copy()
        embedding_vector2 = embedding_vector2.squeeze().to('cpu').detach().numpy().copy()

        return embedding_vector1, embedding_vector2

    def identfy(self):
        '''
        identfy to compute cosine similarity between preproc_embedding_vector1 and preproc_embedding_vector2
        Returns:
            degree_of_similarity[np.array]

        '''

        preproc_embedding_vector1, preproc_embedding_vector2 = self.__preprocess(self.embedding_vector1, self.embedding_vector2)
        self.degree_of_similarity = self.__cos_similarity(preproc_embedding_vector1, preproc_embedding_vector2)

        return self.degree_of_similarity

    def is_candidate_suspicious(self):
        '''

        Returns:

        '''

        return self.degree_of_similarity < self.TH

