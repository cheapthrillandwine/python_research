import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("68.png", cv2.IMREAD_COLOR)
bi = cv2.bilateralFilter(img, 15, 50, 50)
bi2 = cv2.bilateralFilter(bi, 15, 50, 50)
bi3 = cv2.bilateralFilter(bi2, 15, 50, 50)

# plt.subplot(2,2,1),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.title('Original')
# plt.xticks([]),plt.yticks([])

# plt.subplot(2,2,2),plt.imshow(cv2.cvtColor(bi, cv2.COLOR_BGR2RGB))
# plt.title('bi')
# plt.xticks([]),plt.yticks([])
#
# plt.subplot(2,2,3),plt.imshow(cv2.cvtColor(bi2, cv2.COLOR_BGR2RGB))
# plt.title('bi2')
# plt.xticks([]),plt.yticks([])

plt.subplot(1,1,1),plt.imshow(cv2.cvtColor(bi3, cv2.COLOR_BGR2RGB))
plt.title('bi3')
plt.xticks([]),plt.yticks([])

plt.show()


keycode = cv2.waitKey(0)

if keycode == ord('s'):
    plt.imwrite("bi.png", bi)
    plt.imwrite("bi2.png", bi2)
    plt.imwrite("bi3.png", bi3)
