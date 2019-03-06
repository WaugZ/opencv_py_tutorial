import numpy as np
import cv2
import matplotlib.pyplot as plt

m = cv2.imread("C:\\Users\\38345\\Desktop\\map.jpg")
h, w = m.shape[:2]
m = cv2.resize(m, (int(w / 2), int(h / 2)))
h, w = m.shape[:2]
# plt.imshow(m)
# plt.show()

src_pt = np.float32([[0, 0], [100, 0], [0, 100], [100, 100]])
# src_pt1 = np.array([[0, 0], [100, 0], [0, 100], [100, 100]])
dst_pt = np.float32([[5, 5], [90, 5], [5, 90], [90, 90]])
# dst_pt = src_pt
t = cv2.getPerspectiveTransform(src_pt, dst_pt)
dst = cv2.warpPerspective(m, t, (w, h))

cv2.imshow("dst", dst)
cv2.waitKey()
# print("Hello World.")
