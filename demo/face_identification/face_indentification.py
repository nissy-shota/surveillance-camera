#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

from facenet_pytorch import InceptionResnetV1


class FaceIdentificator:

    def __init__(self, detected_face):

        self.detected_face = detected_face

    def identify(self):

        resnet = InceptionResnetV1(pretrained='vggface2').eval()
        embedding_vector = resnet(self.detected_face.unsqueeze(0))

        return embedding_vector

