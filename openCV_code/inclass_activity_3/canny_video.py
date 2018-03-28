import cv2
import numpy as np

videoCap = cv2.VideoCapture(0)

ret, nextFrame = videoCap.read()

while ret:
    # Deal with the canny
    gray_image = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(gray_image, 50, 200)

    # Deal with Houghlines
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180,
                            threshold=5, minLineLength=20, maxLineGap=10)

    for lineSet in lines:
        for line in lineSet:
            cv2.line(nextFrame, (line[0], line[1]),
                     (line[2], line[3]), (0, 0, 255), 3, 8)


    cv2.imshow("Video", nextFrame)

    key_stroke = chr(cv2.waitKey(1) & 0xff)

    if key_stroke == "q":
        break
    else:
        ret, nextFrame = videoCap.read()
