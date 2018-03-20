import cv2
import numpy as np
import random

image = cv2.imread("../TestImages/beachBahamas.jpg")

if image is None:
    print("===> ERROR READING IMAGE")

(b, g, r) = cv2.split(image)
channels = [b, g, r]

for i in range(4):
    random.shuffle(channels)
    newImage = cv2.merge(channels)

    cv2.imshow("Shuffled image", newImage)
    cv2.waitKey(0)
