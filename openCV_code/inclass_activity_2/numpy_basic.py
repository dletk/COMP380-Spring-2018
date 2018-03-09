import cv2
import numpy as np

image = cv2.imread("../TestImages/SnowLeo4.jpg")

if image is None:
    print("Error reading the image")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray image", gray)

blankImage = np.zeros((150, 250), np.uint8)

cv2.imshow("Blank image", blankImage)

cv2.waitKey(0)
