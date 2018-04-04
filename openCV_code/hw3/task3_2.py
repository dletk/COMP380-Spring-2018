import cv2
import numpy as np

default = input("Enter D to use default value or M to enter manually: ")
if default in "mM":
    hueLower = int(input("Enter the lower bound for HUE: "))
    hueUpper = int(input("Enter the upper bound for HUE: "))
else:
    hueLower = 30
    hueUpper = 70

videoCap = cv2.VideoCapture(0)
ret, frame = videoCap.read()

while ret:
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(frame)

    # Find all the pixels that have the HSV value be in range.
    # Notice: All the ranges needs to be satisfied, not only one of H,S or V.
    mask = cv2.inRange(frame, np.array([hueLower, 100, 100]), np.array([hueUpper, 255, 255]))
    mask = cv2.merge((mask, mask, mask))

    # Using the mask to mask out all the out of range pixel
    filtered_frame = cv2.bitwise_and(frame, mask)

    hueNew, Snew, gray_image = cv2.split(filtered_frame)

    # Enhanced the details to make finding contours easier.
    dilated_kernel = (100, 100)
    dilated_image = cv2.dilate(gray_image, dilated_kernel, iterations=10)
    erode_kernel = (5,5)
    eroded_image = cv2.erode(dilated_image, erode_kernel, iterations=10)

    # Find all the contours. Using cv2.RETR_EXTERNAL because we are only interested in
    # the outermost contours, i.e., the contours bound a whole object.
    image, contours, hier = cv2.findContours(
        eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the bounding rectanle
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
