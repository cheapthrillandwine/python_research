import cv2
import numpy as np

img = cv2.imread("meter_gas.jpg")

print(img.shape)
print(img.shape[1], img.shape[0])

# cv2.imshow("img", img)
# cv2.waitKey(27)
# cv2.destroyAllWindows()
