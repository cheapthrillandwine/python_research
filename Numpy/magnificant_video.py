# -*- coding: utf-8 -*-
import cv2
import numpy as np
#画像を読み込む

#マウスの操作のコールバック関数
def callback(event, x, y, flags, param):
    global frame, frame_win, sx, sy, rect, abs_x, abs_y, abs_sx, abs_sy
    abs_x, abs_y = rect[0] + x, rect[1] + y
    #拡大領域の始点
    if event == cv2.EVENT_RBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y
    #拡大領域の選択
    if flags == cv2.EVENT_FLAG_RBUTTON:
        frame_win = frame.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
        cv2.rectangle(frame_win, (sx, sy), (x, y), (0, 0, 0), 2)
    #拡大結果の出力
    if event == cv2.EVENT_RBUTTONUP:
        rect_x = np.clip(min(abs_sx, abs_x), 0, frame.shape[1] - 2)
        rect_y = np.clip(min(abs_sy, abs_y), 0, frame.shape[0] - 2)
        rect_w = np.clip(abs(abs_sx - abs_x), 1, frame.shape[1] - rect_x)
        rect_h = np.clip(abs(abs_sy - abs_y), 1, frame.shape[0] - rect_y)
        rect = (rect_x, rect_y, rect_w, rect_h)
        frame_win = frame.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
    #左クリックしたら移動の始点を決定
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
        abs_sx, abs_sy = abs_x, abs_y
    #マウスの動きに合わせて画面移動
    if flags == cv2.EVENT_FLAG_LBUTTON:
        rect_x = np.clip(rect[0] + abs_sx - abs_x, 0, frame.shape[1] - rect[2])
        rect_y = np.clip(rect[1] + abs_sy - abs_y, 0, frame.shape[0] - rect[3])
        rect_w = rect[2]
        rect_h = rect[3]
        rect = (rect_x, rect_y, rect_w, rect_h)
        frame_win = frame.copy()[rect[1]:rect[1]+rect[3], rect[0]:rect[0] + rect[2]]
# cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
# cv2.setMouseCallback("frame", callback)
# while(1):
    cv2.imshow("frame", frame_win)
#     k = cv2.waitKey(1)
#     #Escキーを押すと終了
#     if k == 27:
#         break
#
#     #拡大をリセット
#     if k == ord("r"):
#         rect = (0, 0, frame.shape[1], frame.shape[0])
#         frame_win = frame.copy()

if __name__ == '__main__':

    cap = cv2.VideoCapture("gas_meter.mp4")
    wname = "Magnificant" # Window name
    cv2.namedWindow(wname)

    # print(type(pts)) # class __main__.PointList()
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_win = frame.copy()
        rect = (0, 0, frame.shape[1], frame.shape[0])
        cv2.setMouseCallback(wname, callback)
        cv2.imshow(wname, frame_win)
        k = cv2.waitKey(1)
        if k == 27:
            break
        if k == ord("r"):
            rect = (0, 0, frame.shape[1], frame.shape[0])
            frame_win = frame.copy()
    cap.release()
    cv2.destroyAllWindows()
