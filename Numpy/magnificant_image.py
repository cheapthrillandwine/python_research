# -*- coding: utf-8 -*-
import cv2
import numpy as np
#画像を読み込む
img = cv2.imread("meter_gas.jpg")
# img_resize = cv2.resize(img, (300, 300))
img_win = img.copy() # 取得画像のコピー
rect = (0, 0, img.shape[1], img.shape[0])
 # 矩形のパラメータ


'''
img_winはウィンドに表示する画像です。
x, yはウィンド内のマウスの位置です。
sx, syはウィンド内の拡大領域の始点です。
rectは現在表示されている領域の位置とサイズです。
abs_x, abs_yは画像内のマウスの位置です。
abs_sx, abs_syは画像内の拡大領域の始点です。
'''

#マウスの操作のコールバック関数
def callback(event, x, y, flags, param):
    global img, img_win, sx, sy, rect, abs_x, abs_y, abs_sx, abs_sy
    abs_x, abs_y = rect[0] + x, rect[1] + y
    #拡大領域の始点
    if event == cv2.EVENT_RBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y
        print(sx, sy)
        # print(abs_sx, abs_sy)
    #拡大領域の選択
    if flags == cv2.EVENT_FLAG_RBUTTON:
        img_win = img.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
        cv2.rectangle(img_win, (sx, sy), (x, y), (0, 0, 0), 2)
    #拡大結果の出力
    if event == cv2.EVENT_RBUTTONUP:
        print(abs_sx, abs_x)
        rect_x = np.clip(min(abs_sx, abs_x), 0, img.shape[1] - 2)
        rect_y = np.clip(min(abs_sy, abs_y), 0, img.shape[0] - 2)
        rect_w = np.clip(abs(abs_sx - abs_x), 1, img.shape[1] - rect_x)
        rect_h = np.clip(abs(abs_sy - abs_y), 1, img.shape[0] - rect_y)
        rect = (rect_x, rect_y, rect_w, rect_h)
        img_win = img.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]

        cv2.imshow("resize", img_win)
    #左クリックしたら移動の始点を決定
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y
    #マウスの動きに合わせて画面移動
    if flags == cv2.EVENT_FLAG_LBUTTON:
        rect_x = np.clip(rect[0] + abs_sx - abs_x, 0, img.shape[1] - rect[2])
        rect_y = np.clip(rect[1] + abs_sy - abs_y, 0, img.shape[0] - rect[3])
        rect_w = rect[2]
        rect_h = rect[3]
        rect = (rect_x, rect_y, rect_w, rect_h)
        img_win = img.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("img", callback)
while(1):
    cv2.imshow("img", img_win)
    k = cv2.waitKey(1)
    #Escキーを押すと終了
    if k == 27:
        break

    #拡大をリセット
    if k == ord("r"):
        rect = (0, 0, img.shape[1], img.shape[0])
        img_win = img.copy()
