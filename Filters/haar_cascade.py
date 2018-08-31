'''
この検出器ではHaar-Cascadeによる顔認識を行い、検出したオブジェクトは赤線矩形で囲まれます。
'''
# -*- coding: utf-8 -*-
import cv2
# import numpy as nm
def main():
    # 入力画像読み込み
    img = cv2.imread("capture/sample2.jpg")
    # cv2.imshow("color",img)
    # カスケード型識別器の読み込み
#     cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cascade = cv2.CascadeClassifier(r"opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml")
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔領域の探索
#     face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    # 顔領域を赤色の矩形で囲む
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y+h), (0,0,200), 3)

    # 結果を出力
    cv2.imshow("result.jpg", img)
    cv2.imwrite("result.jpg", img)
if __name__ == '__main__':
    main()

'''
パラメータ名:	説明
path:	使用するカスケード識別器のファイルパス
src:	入力画像
scaleFactor:	画像スケールにおける縮小量
minNeighbors:	矩形を要素とするベクトル
minSize:	探索窓の最小サイズ（これより小さい対象は無視）
face:	探索結果（見つかった場所の左上座標・幅・高さを格納したリスト）
'''
