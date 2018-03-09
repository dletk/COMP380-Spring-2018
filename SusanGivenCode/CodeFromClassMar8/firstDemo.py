

import cv2


img1 = cv2.imread("../TestImages/beachBahamas.jpg")

if img1 is None:
    print("FAILED TO READ FILE!")


print(img1)
cv2.imshow("Beach", img1)

cv2.waitKey()