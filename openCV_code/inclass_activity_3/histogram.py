import cv2

original_image = cv2.imread("../TestImages/SnowLeo4.jpg")

gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

newImage = cv2.equalizeHist(gray_image)

cv2.imshow("Original", original_image)
cv2.imshow("Original gray", gray_image)
cv2.imshow("Histogram", newImage)
cv2.waitKey(0)
