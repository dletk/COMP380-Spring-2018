import cv2
import numpy as np

image = cv2.imread("../TestImages/shops.jpg")

# Crop the image in the order : row, col (this is from NumPy) ===> height, width
subImage = image[0:100, 0:200]

cv2.imshow("Image cropped", subImage)
cv2.waitKey(0)
