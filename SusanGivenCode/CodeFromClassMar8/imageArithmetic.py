import cv2
import numpy as np

img1 = cv2.imread("../../openCV_code/TestImages/beachBahamas.jpg")
img2 = cv2.imread("../../openCV_code/TestImages/Landscape1MuchSmaller.jpg")

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)

print("Original:", img2[0,0,:])
newImgA = img2  + 50

fifties = np.zeros(img2.shape, np.uint8) + 50
newImgB = cv2.add(img2, fifties)

print("NUMPY:", newImgA[0,0,:])
print("OpenCV:", newImgB[0,0,:])

cv2.imshow("New Numpy", newImgA)
cv2.imshow("New OpenCV", newImgB)

cv2.waitKey()

cv2.destroyAllWindows()







# newIm = 50 + np.zeros(img2.shape, np.uint8)
# newImgC = cv2.add(img2, newIm)
# cv2.imshow("Second OpenCV", newImgC)
#
# print("Numpy value:", newImgA[0,0,:])
# print("OpenCV value:", newImgB[0,0,:])
# print("Final value:", newImgC[0,0,:])
#
