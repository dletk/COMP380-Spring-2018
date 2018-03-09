

import cv2

img1 = cv2.imread("TestImages/beachBahamas.jpg")
img2 = cv2.imread("TestImages/Landscape1MuchSmaller.jpg")

img3 = cv2.imread("TestImages/Blowhole013.jpg")
img4 = cv2.imread("TestImages/Blowhole021.jpg")

cv2.imshow("B1", img3)
cv2.imshow("B2", img4)
diff = cv2.absdiff(img3, img4)
cv2.imshow("Diff", diff)

cv2.waitKey()

negIm1 = 255 - img1
cv2.imshow("Negative", negIm1)

cv2.waitKey()

(hgt1, wid1, dep1) = img1.shape
(hgt2, wid2, dep2) = img2.shape

minHgt = min(hgt1, hgt2)
minWid = min(wid1, wid2)

img1ROI = img1[0:minHgt, 0:minWid, :]
img2ROI = img2[0:minHgt, 0:minWid, :]

wt = 0.5
while True:
    blendIm = cv2.addWeighted(img1ROI, wt,  img2ROI, 1.0 - wt, 0)
    cv2.imshow("Blended", blendIm)
    x = cv2.waitKey(0)
    ch = chr(x & 0xFF)
    if ch == 'q':
        break
    elif ch == 'd':
        wt = min(1.0, wt + 0.1)
    elif ch == 'a':
        wt = max(0.0, wt - 0.1)

cv2.destroyAllWindows()
