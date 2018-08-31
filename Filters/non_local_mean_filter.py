import numpy as np
import cv2
from matplotlib import pyplot as plt

# 画像用コード
# original = cv2.imread('test.jpg') # pngだとチャネル数が合わないようです。
# img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
# dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
# # plt.subplot(2,1,1),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# # plt.title("original")
# # plt.xticks([]),plt.yticks([])
# # plt.subplot(2,1,2),plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
# # plt.title("NLMeans")
# # plt.show()
# plt.subplot(121),plt.imshow(img)
# plt.subplot(122),plt.imshow(dst)
# plt.show()

# ------------------------------------------------------------------------------
# 動画用コード
def main():

    # 動画の読み込み
    cap = cv2.VideoCapture('privacy.wmv')
    # original = cv2.VideoCapture('IMG_3984.mp4')
    # cap = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    # 動画終了まで繰り返し
    while(cap.isOpened()):
        # フレーム取得
        ret, frame = cap.read()
        # 色空間の変更
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            dst = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        # フレームを表示
        cv2.imshow("nlmf", dst)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
