import cv2

original_image = cv2.imread("../TestImages/Coins1.jpg")
cv2.imshow("Original", original_image)

# Enhanced the edges in the image
enhanced_edges_image = cv2.morphologyEx(
    original_image, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)))

# Remove some noises in the background
enhanced_edges_image = cv2.GaussianBlur(enhanced_edges_image, (11,11), 0)

# cv2.imshow("Enhanced edges", enhanced_edges_image)

ret, thresholded = cv2.threshold(enhanced_edges_image, 5, 255, cv2.THRESH_BINARY_INV)

gray_image = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)

im2, contours, hier = cv2.findContours(
    gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

output = cv2.drawContours(original_image, contours, -1, (0, 255, 0), 2)

# cv2.imshow("Gray", gray_image)
# cv2.imshow("Thresholded", thresholded)
cv2.imshow("Find Coin", output)

cv2.waitKey(0)
