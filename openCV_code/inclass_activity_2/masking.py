import cv2
import numpy
img = cv2.imread("../TestImages/SnowLeo4.jpg")
gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(height, width, depth) = img.shape
mask = numpy.zeros((height, width, 1), numpy.uint8)

mask[50:height // 2, 50:width // 2] = 255

maskedImg1 = cv2.bitwise_and(gImg, mask)
cv2.imshow("Original", gImg)
cv2.imshow("Masked", maskedImg1)
cv2.waitKey(0)

colorMask = cv2.merge((mask, mask, mask))
maskedImg2 = cv2.bitwise_and(img, colorMask)
cv2.imshow("Original", img)
cv2.imshow("Masked", maskedImg2)
cv2.waitKey(0)

cv2.destroyAllWindows()
