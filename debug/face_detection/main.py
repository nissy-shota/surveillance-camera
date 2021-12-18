import os
from face_detector import FaceDetector

IMG_DIR = '/home/shota/Projects/surveillance-camera/debug/face_detection/img'
RESULTS_DIR = '/home/shota/Projects/surveillance-camera/debug/face_detection/results'

def main():

    sample_img_path = os.path.join(IMG_DIR, 'tubasa.jpg')
    detector = FaceDetector(sample_img_path)
    detector.detecte_face()
    save_path = os.path.join(RESULTS_DIR, 'clopped.jpg')
    detector.save(save_path)
    detector.show()


if __name__ == "__main__":
    main()