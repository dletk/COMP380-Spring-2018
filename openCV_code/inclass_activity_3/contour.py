import cv2

original_image = cv2.imread("../TestImages/Coins1.jpg")
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Original", original_image)
cv2.imshow("Original gray", gray_image)

# gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

ret, thresh = cv2.threshold(gray_image, 130, 255, cv2.THRESH_BINARY)

im2, contrs, hier = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(original_image, contrs, -1, (0, 255, 0), 1)

cv2.imshow("Contours", original_image)

cv2.waitKey(0)
