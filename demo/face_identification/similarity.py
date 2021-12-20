#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import numpy as np


class ComputeSimilarity:

    def __init__(self, embedding_vector1, embedding_vector2, TH = 0.7):

        self.embedding_vector1 = embedding_vector1
        self.embedding_vector2 = embedding_vector2

    def __cos_similarity(self, embedding_vector1, embedding_vector2):

        return np.dot(embedding_vector1, embedding_vector2) / (np.linalg.norm(embedding_vector1) * np.linalg.norm(embedding_vector2))

    def __preprocess(self, embedding_vector1, embedding_vector2):

        embedding_vector1 = embedding_vector1.squeeze().to('cpu').detach().numpy().copy()
        embedding_vector2 = embedding_vector2.squeeze().to('cpu').detach().numpy().copy()

        return embedding_vector1, embedding_vector2

    def compute_similarity(self):

        preproc_embedding_vector1, preproc_embedding_vector2 = self.__preprocess(self.embedding_vector1, self.embedding_vector2)
        degree_of_similarity = self.__cos_similarity(preproc_embedding_vector1, preproc_embedding_vector2)

        return degree_of_similarity
