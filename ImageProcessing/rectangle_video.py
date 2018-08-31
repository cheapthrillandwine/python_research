import cv2
import numpy as np

def main():
    # import image
    # img = "images/rect_gauge1.jpg"
    cap = cv2.VideoCapture(0)

    while(True):
    # Capture frame-by-frame
        ret, frame = cap.read()

        frame = cv2.resize(frame, (600,600))

    # src = cv2.imread(img,1)     # color(default)
    # src = cv2.imread(img,0)   # grayscale
    # src = cv2.imread(img,-1)  # alfachannel

    # get image size
        # h, w, channels = frame.shape
        #
        # img_size = h * w

        # conversion to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Edge smoothing
        gray = cv2.GaussianBlur(gray, (5,5), 1)

        # threshold(necessary to manual setting for 2th argument)
        ret, dst = cv2.threshold(gray,200,255,0)

        # Define neiborhood4
        neiborhood4 = np.array([[0,1,0],
                                [1,1,1],
                                [0,1,0]],
                                np.uint8)
        # Define neiborhood8
        neiborhood8 = np.array([[1,1,1],
                                [1,1,1],
                                [1,1,1]],
                                np.uint8)

        # ８近傍で膨張処理
        dst = cv2.dilate(dst,neiborhood8,iterations=1)

        # inverted black to white
        dst = cv2.bitwise_not(dst)
        cv2.imshow('pre_frame',dst)
        # re-filtering
        ret, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # extract contours
        dst, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # export debug image
        # dst = cv2.imread(img, 1)
        # dst = cap.read(frame)
        dst = cv2.drawContours(dst, contours, -1, (0, 0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imwrite("debug_1.jpg", dst)

            # draw bounding rectangle
        for i, contour in enumerate(contours):
            # 小さな領域の場合は間引く
            area = cv2.contourArea(contour)
            if area < 1000:
                continue

            # 画像全体を占める領域は除外する
            # if img_size * 0.99 < area:
            #     continue

            # 外接矩形を取得
            x,y,w,h = cv2.boundingRect(contour)
            dst = cv2.rectangle(dst,(x,y),(x+w,y+h),(0,255,0),2)
            x1 = x
            y1 = y
            x2 = x+w
            y2 = y+h
            # 座標は左上、右上、左下、右下の順番
            # 外接矩形の座標及び、サイズでリサイズを行う。
            pts1 = np.float32([[x1,y1],[x2,y1],[x1,y2],[x2,y2]])
            pts2 = np.float32([[0,0],[600,0],[0,600],[600,600]])

            M = cv2.getPerspectiveTransform(pts1,pts2)
            # width, heightの順番
            dst = cv2.warpPerspective(dst,M,(600,600))

        # show window
        # cv2.imshow("result.jpg", dst)
            cv2.imshow('original_frame',frame)
            cv2.imshow('result_frame',dst)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # save result
    # cv2.imwrite("result.jpg", dst)

    # hold window
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
