#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import numpy as np

from facenet_pytorch import InceptionResnetV1


class FaceFeatureExtractor:

    def __init__(self, detected_face):

        self.detected_face = detected_face

    def feature_extraction(self):

        resnet = InceptionResnetV1(pretrained='vggface2').eval()
        embedding_vector = resnet(self.detected_face.unsqueeze(0))

        return embedding_vector


class FaceIdentificator:

    def __init__(self, embedding_vector1, embedding_vector2, TH = 0.7):

        self.embedding_vector1 = embedding_vector1
        self.embedding_vector2 = embedding_vector2
        self.TH = TH

    def __cos_similarity(self, embedding_vector1, embedding_vector2):

        return np.dot(embedding_vector1, embedding_vector2) / (np.linalg.norm(embedding_vector1) * np.linalg.norm(embedding_vector2))

    def __preprocess(self, embedding_vector1, embedding_vector2):

        embedding_vector1 = embedding_vector1.squeeze().to('cpu').detach().numpy().copy()
        embedding_vector2 = embedding_vector2.squeeze().to('cpu').detach().numpy().copy()

        return embedding_vector1, embedding_vector2

    def identfy(self):

        preproc_embedding_vector1, preproc_embedding_vector2 = self.__preprocess(self.embedding_vector1, self.embedding_vector2)
        self.degree_of_similarity = self.__cos_similarity(preproc_embedding_vector1, preproc_embedding_vector2)

        return self.degree_of_similarity

    def is_candidate_suspicious(self):

        return self.degree_of_similarity < self.TH

