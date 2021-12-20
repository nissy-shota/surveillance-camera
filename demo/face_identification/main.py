#  Copyright (c) 2021.
#  Shota Nishiyama
#  All rights reserved.

import gc
import os

from face_detector_deep import FaceDetector
from face_indentification import FaceIdentificator
from face_indentification import FaceFeatureExtractor

IMG_DIR = '/home/shota/Projects/surveillance-camera/demo/face_identification/images'


def main():

    # load sample images
    file_name1 = os.path.join(IMG_DIR, 'HikaruUtada1.jpg')
    file_name2 = os.path.join(IMG_DIR, 'MisatoUgaki.jpg')

    # face detecte from image
    detector = FaceDetector(file_name1)
    cropped_face_img1 = detector.detecte_face()
    detector.show()
    del detector
    gc.collect()

    detector = FaceDetector(file_name2)
    cropped_face_img2 = detector.detecte_face()
    detector.show()
    del detector
    gc.collect()

    # face feature extraction
    feature_extractor = FaceFeatureExtractor(cropped_face_img1)
    face_embedding_vector1 = feature_extractor.feature_extraction()
    del feature_extractor
    gc.collect()

    feature_extractor = FaceFeatureExtractor(cropped_face_img2)
    face_embedding_vector2 = feature_extractor.feature_extraction()
    del feature_extractor
    gc.collect()

    # face identficate between 2 images.
    face_identificator = FaceIdentificator(face_embedding_vector1, face_embedding_vector2)
    degree_of_similarity = face_identificator.identfy()
    print(f'degree of similarity is {degree_of_similarity:.4} between {file_name1} and {file_name2}.')

    # judge and notification
    if face_identificator.is_candidate_suspicious():
        print('We\'ve detected a potential prowler, and we\'ve sent a notification to your LINE.')
        print('take care.')
        # TODO (shota.nishiyama44@gmail) to call line sender
    else:
        print('Your house is safe.')


if __name__ == "__main__":
    main()