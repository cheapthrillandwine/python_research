import numpy as np
import cv2
from matplotlib import pyplot as plt

img_src = cv2.imread("test.jpg")
img_dst = cv2.GaussianBlur(img_src, (5,5), 1)

plt.subplot(121),plt.imshow(img_src),plt.title('Original')
plt.xticks([]),plt.yticks([])

plt.subplot(122),plt.imshow(img_dst),plt.title('Blurred')
plt.xticks([]),plt.yticks([])
plt.show()
# plt.imshow(img_src)
# plt.imshow(img_dst)
