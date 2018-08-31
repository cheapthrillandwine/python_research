import numpy as np
import cv2
from matplotlib import pyplot as plt

# cap = cv2.VideoCapture('IMG_3984.mp4')
# bi = cv2.bilateralFilter(cap, 15, 50, 50)
#
# plt.subplot(1,1,1),plt.imshow(cv2.cvtColor(bi, cv2.COLOR_BGR2RGB))
# plt.title('Bilateral')
# plt.xticks([]),plt.yticks([])
#
# plt.show()
#
# while(bi.isOpened()):
#     ret, frame = bi.read()
#     if ret == True:
#         # frame = cv2.flip(frame,0) # 縦方向に反転する
#     # video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 顔が青くなっちゃう
#
#         cv2.imshow('Original',frame)
#         if cv2.waitKey(50) & 0xFF == ord('q'):
#             break
#
#     else:
#         break
# cap.release()
# cv2.destroyAllWindows()
#
# ------------------------------------------------------------------------------
def main():

    # 動画の読み込み
    # cap = cv2.VideoCapture('IMG_3984.mp4')
    cap = cv2.VideoCapture('privacy.wmv')

    # 動画終了まで繰り返し
    while(cap.isOpened()):
        # フレーム取得
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.bilateralFilter(frame, 15, 25, 25)
            frame2 = cv2.bilateralFilter(frame, 15, 50, 50)
            # frame3 = cv2.bilateralFilter(frame2, 15, 50, 50)
            # plt.subplot(1,1,1),plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # plt.title('Bilateral')
            # plt.xticks([]),plt.yticks([])
            #
            # plt.show()
        # フレームを表示
        # cv2.imshow("Bilateral1", frame)
        cv2.imshow("Bilateral2", frame2)
        # cv2.imshow("Bilateral3", frame3)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
