import cv2

image = cv2.imread("../TestImages/SnowLeo4.jpg")

edges = cv2.Canny(image, 100, 200)

cv2.imshow("Edges", edges)
cv2.waitKey(0)
