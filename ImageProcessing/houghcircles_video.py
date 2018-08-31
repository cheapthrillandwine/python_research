import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False

while(ret):
    cv2.waitKey(1)
    ret, frame = cap.read()
    # ミラー
    # frame = frame[:,::-1]
    # size = (640,480)
    # frame = cv2.resize(frame, size)
    img = cv2.medianBlur(frame,5)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 60, param1=50, param2=90, minRadius=50, maxRadius=100)

    if circles is None:
        cv2.imshow("preview", frame)
        continue
        # circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        print(i)
        # 囲み線を描く
        cv2.circle(frame,(i[0],i[1]),i[2],(255,255,0),2)
        # 中心点を描く
        cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('preview', frame)

    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#
# while(True):
#     ret, frame = cap.read()
#     # frame = frame[:,::-1]
#     size = (640,480)
#     frame = cv2.resize(frame, size)
#     frame = cv2.medianBlur(frame,5)
#     cimg = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
#
#     circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,20,param1=50,param2=85,minRadius=0,maxRadius=0)
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         # draw the outer circle
#         cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#         # draw the center of the circle
#         cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
#
#
#         cv2.imshow('preview', cimg)
#         if cv2.waitKey(33) & 0xFF == ord('q'):
#             break
# cap.release()
# cv2.destroyAllWindows()
