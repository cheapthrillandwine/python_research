import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
# 画像用コード
# src = cv2.imread('test.jpg')
# # flagsは1=RECUR_FILTER 2=NORMCONV_FILTERで1は精度がやや低いが高速なので推奨
# dst = cv2.edgePreservingFilter(src, flags=1, sigma_s=60, sigma_r=0.4)
#
# plt.subplot(2,1,1),plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
# plt.title("src")
# plt.xticks([]),plt.yticks([])
# plt.subplot(2,1,2),plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
# plt.title("dst")
# plt.show()

# ------------------------------------------------------------------------------
# 動画用コード
def main():

    # 動画の読み込み
    # cap = cv2.VideoCapture('IMG_3984.mp4')
    cap = cv2.VideoCapture('privacy.wmv')

    # 動画終了まで繰り返し
    while(cap.isOpened()):
        # フレーム取得
        ret, frame = cap.read()
        if ret == True:
            # フレームの速度計測
            t = time.time()
            frame = cv2.edgePreservingFilter(frame, flags=1, sigma_s=80, sigma_r=0.4)
            print('[INFO] elapsed time: {:.4f}'.format(time.time() - t))
        # フレームを表示
        cv2.imshow("edgePreserving", frame)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
