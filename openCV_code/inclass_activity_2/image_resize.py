import cv2
import numpy as np

image = cv2.imread("../TestImages/beachBahamas.jpg")

resize_image = cv2.resize(image, (300,300))

cv2.imshow("Original image", image)
cv2.imshow("Resized image", resize_image)
cv2.waitKey(0)
