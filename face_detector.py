import cv2

class HaarFaceDetector:
    
    # 顔検出モデルのパス
    cascade_path = ""
    
    def __init__(self, model_path):
        self.cascade_path = model_path

    def getFaceImage(self, rgb_image):
        gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
        
        #カスケード分類器の特徴量を取得する
        cascade = cv2.CascadeClassifier(self.cascade_path)
        
        #顔認識の実行
        facerect = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=2, minSize=(200, 200))
        
        color = (255, 255, 255) #白
        
        if len(facerect) == 1:
            #検出した顔を囲む矩形の作成
            for rect in facerect:
                #TODO:画角から出た場合のエラー処理を書く
                rect[0] -= 100; rect[1] -= 100; rect[2] += 200; rect[3] += 200; 
                # cv2.rectangle(rgb_image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
                face_image = rgb_image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                return (face_image)
