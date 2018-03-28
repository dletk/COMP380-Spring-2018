import cv2

img = cv2.imread("../TestImages/SnowLeo4.jpg")

cv2.imshow("Original image", img)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, img_thresheld = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY_INV)

cv2.imshow("Thresholded", img_thresheld)

cv2.waitKey(0)
