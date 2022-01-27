import cv2
import glob

from torch import le

# get_face_similarity(対象の顔画像, テンプレートのディレクトリパス) -> 類似度を返す
def get_face_similarity(target_image, template_dir):
    
    # NOTE: target_imageは背景をマスクしておいた方が精度出そう

    # resizeのサイズ
    IMG_SIZE = (200, 200)
    
    # BFMatcherオブジェクトの生成
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    target_image = cv2.resize(target_image, IMG_SIZE)
    # 顔画像の入力（カラー）
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    # AKAZEを適用、特徴点を検出
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_image, None)
    
    #　templateディレクトリ内のファイルパスを取得
    files = glob.glob(template_dir)
    
    similarity_list = [] # 類似度を記録するリスト
    
    for file in files:
        # .jpgのみ有効
        if not('.jpg' in file):
            continue
        
        try:
            template_img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            template_img = cv2.resize(template_img, IMG_SIZE)
            
            (template_kp, template_des) = detector.detectAndCompute(template_img, None)
            # BFMatcherで総当たりマッチングを行う
            matches = bf.match(target_des, template_des)
            #特徴量の距離を出し、平均を取る
            dist = [m.distance for m in matches]
            similarity_list.append(sum(dist) / len(dist)) # retが類似度
            
        except cv2.error:
            similarity_list.append(10000)
    
    if len(similarity_list) == 0:
        return -1
    
    #　一番似てる画像の類似度を返す
    return min(similarity_list)