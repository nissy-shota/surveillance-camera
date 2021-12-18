import os

from facenet_pytorch import MTCNN, InceptionResnetV1
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


IMG_DIR = '/home/shota/Projects/surveillance-camera/debug/face_detection/img'

def main():

    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    image_path = os.path.join(IMG_DIR, 'tubasa.jpg')
    img = Image.open(image_path)
    img_cropped = mtcnn(img)

    detected_img = img_cropped.to('cpu').detach().numpy().copy()
    detected_img = np.transpose(detected_img, (1, 2, 0))
    print(detected_img.shape)
    plt.imshow(detected_img)
    plt.show()




if __name__ == "__main__":
    main()