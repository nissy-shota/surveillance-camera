import cv2
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class FaceDetector:
    '''
    face detection class.
    Attributes:
        img_path (str): image path
        img (PIL): PIL Object which has range (-1, 1)
        img_cropped(tensor): cropped img by mtcnn
        detected_img(numpy array): detecte face image which has range (-1, 1)

    Examples:
        >>> detector = FaceDetector(image_path)
        >>> img_cropped = detector.detecte_face()
        >>> detector.save()
        >>> detector.show()
    '''

    def __init__(self, img_path):
        self.img_path = img_path

    def detecte_face(self):
        '''
        detect face
        Args: None
        return: cropped image
        '''

        mtcnn = MTCNN()
        self.img = Image.open(self.img_path)
        self.img_cropped = mtcnn(self.img)

        return self.img_cropped

    def save(self, save_path):
        '''
        save face image
        Args: save_path
        return: None
        '''
        detected_img = self.img_cropped.to('cpu').detach().numpy().copy()
        self.detected_img = np.transpose(detected_img, (1, 2, 0))
        cv2.imwrite(save_path, self.detected_img)

    def show(self):

        '''
        show face image
        Args: save_path
        return: None
        '''
        detected_img = self.img_cropped.to('cpu').detach().numpy().copy()
        self.detected_img = np.transpose(detected_img, (1, 2, 0))
        plt.imshow(self.detected_img)
        plt.show()
