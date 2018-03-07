import cv2

image = cv2.imread("TestImages/SnowLeo2.jpg")

# Draw a cile around the leopard's head
cv2.circle(image, (120, 130), 70, (207, 142, 27), thickness=3)

# Draw a rectangle over its body
cv2.rectangle(image, (190, 100), (530, 300), (0, 0, 120), thickness=cv2.FILLED)

# Draw some lines as the tail
for i in range(4):
    cv2.line(image, (530, 120), (530 + 10 * (i + 1), 250),
             (0, 255, 255), thickness=2)

cv2.putText(image, "SnowLeo2.jpg", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

cv2.imshow("Image window", image)
cv2.waitKey(0)
