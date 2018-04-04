import cv2
import numpy as np

default = input("Enter D to use default value or M to enter manually: ")
if default in "mM":
    hueLower = input("Enter the lower bound for HUE: ")
    hueUpper = input("Enter the upper bound for HUE: ")
    # (rLower, gLower, bLower) = [int(x) for x in  rgbLower.split("-")]
    # (rUpper, gUpper, bUpper) = [int(x) for x in  rgbUpper.split("-")]
else:
    # (rLower, gLower, bLower) = [90, 95, 10]
    # (rUpper, gUpper, bUpper) = [150, 150, 40]
    hueLower = 30
    hueUpper = 70

videoCap = cv2.VideoCapture(0)
ret, frame = videoCap.read()

while ret:
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(frame)

    # Filter the image to prepare the mask
    # res, threshR = cv2.threshold(r, rLower, rUpper, cv2.THRESH_TOZERO)
    # res, threshG = cv2.threshold(g, gLower, gUpper, cv2.THRESH_TOZERO)
    # res, threshB = cv2.threshold(b, bLower, bUpper, cv2.THRESH_TOZERO)

    mask = cv2.inRange(frame, np.array([hueLower, 100, 100]), np.array([hueUpper, 255, 255]))
    mask = cv2.merge((mask, mask, mask))

    print(frame[360][640])

    filtered_frame = cv2.bitwise_and(frame, mask)

    # gray_image = cv2.cvtColor(filtered_frame, cv2.COLOR_HSV2GRAY)
    hueNew, Snew, gray_image = cv2.split(filtered_frame)

    dilated_kernel = (100, 100)
    dilated_image = cv2.dilate(gray_image, dilated_kernel, iterations=10)
    erode_kernel = (5,5)
    eroded_image = cv2.erode(dilated_image, erode_kernel, iterations=10)

    image, contours, hier = cv2.findContours(
        eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, width, height) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y),
                      (x + width, y + height), (255, 0, 0), 2)

    cv2.imshow("Webcam", eroded_image)
    cv2.imshow("Original", frame)

    keyStroke = chr(cv2.waitKey(1) & 0xff)
    if keyStroke in "Qq":
        cv2.destroyAllWindows()
        break

    ret, frame = videoCap.read()
