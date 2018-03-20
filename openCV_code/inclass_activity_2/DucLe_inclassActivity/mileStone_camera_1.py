import cv2
import numpy as np
import random

videoCap = cv2.VideoCapture(0)

ret, frame = videoCap.read()

# Disco effect
while ret:
    (b, g, r) = cv2.split(frame)
    channels = [b, g, r]

    random.shuffle(channels)
    newImage = cv2.merge(channels)

    blur_image = cv2.GaussianBlur(
        newImage, (2 * random.randint(0, 15) + 1, 2 * random.randint(0, 15) + 1), 0)

    cv2.imshow("Webcam", blur_image)
    ret, frame = videoCap.read()

    key_stroke = chr(cv2.waitKey(1) & 0xff)

    if key_stroke == 'q':
        break
