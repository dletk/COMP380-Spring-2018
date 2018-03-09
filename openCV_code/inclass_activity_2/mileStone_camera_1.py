import cv2
import numpy as np
import random

videoCap = cv2.VideoCapture(0)

ret, frame = videoCap.read()

while ret:
    (b, g, r) = cv2.split(frame)
    channels = [b, g, r]

    random.shuffle(channels)
    newImage = cv2.merge(channels)

    cv2.imshow("Webcam", newImage)
    ret, frame = videoCap.read()
    cv2.waitKey(1)
