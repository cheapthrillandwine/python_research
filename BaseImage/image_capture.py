import cv2
import numpy

cap = cv2.videoCapture(0)

while(True):
    ret, frame = cap.read()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imwrite("test", img)
cap.release()
cv2.destroyAllWindows()
