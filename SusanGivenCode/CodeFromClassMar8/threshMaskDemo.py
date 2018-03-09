


import cv2


beach = cv2.imread("TestImages/beachBahamas.jpg")
mountain = cv2.imread("TestImages/Landscape1MuchSmaller.jpg")



grayBeach = cv2.cvtColor(beach, cv2.COLOR_RGB2GRAY)
grayMt = cv2.cvtColor(mountain, cv2.COLOR_RGB2GRAY)

for t in range(0, 255, 25):
    print t
    res, newBeach = cv2.threshold(grayBeach, t, 255, cv2.THRESH_TOZERO)
    cv2.imshow("Thresholded", newBeach)
    cv2.waitKey()

res, thresh = cv2.threshold(grayBeach, 150, 255, cv2.THRESH_TOZERO)
mask = cv2.merge( (thresh, thresh, thresh))
newBeach = cv2.bitwise_and(beach, mask)
cv2.imshow("New Beach", newBeach)
cv2.waitKey()
cv2.destroyAllWindows()