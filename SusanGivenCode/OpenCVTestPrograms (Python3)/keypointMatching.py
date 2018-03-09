
# Sift/Suft Matching Demo


import cv2
import numpy


img1 = cv2.imread("TestImages/DollarCoin.jpg")
img2 = cv2.imread("TestImages/Coins1.jpg")

cv2.imshow("Original 1", img1)
cv2.imshow("Original 2", img2)


# create a SURF object, that can run the SURF algorithm.
# input constant can be varied if not enough or too many keypoints found
orbFinder = cv2.ORB_create(400)

keypts1, des1 = orbFinder.detectAndCompute(img1, None)
print("Image 1, Number of keypoints found:", len(keypts1))

img3 = cv2.drawKeypoints(img1, keypts1, None, (255, 0, 0), 4)
cv2.imshow("Keypoints 1", img3)

keypts2, des2 = orbFinder.detectAndCompute(img2, None)
print("Image 2, Number of keypoints found:", len(keypts2))

img4 = cv2.drawKeypoints(img2, keypts2, None, (255, 0, 0), 4)
cv2.imshow("Keypoints 2", img4)


# Do the matching
FLANN_INDEX_KDTREE = 0
indexParams = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
searchParams = dict(checks=100)
flann = cv2.FlannBasedMatcher(indexParams, searchParams)
matches = flann.knnMatch(des1, des2, k=2)


# keep only the good matches
goodMatches = []
for mat in matches:
    [m, n]= mat
    (m.distance < 0.7 * n.distance) and (m.distance <= 0.5)

    if  (m.distance < 0.7 * n.distance) and (m.distance <= 0.5):
        goodMatches.append(mat)

goodMatches = [x[0] for x in goodMatches]

# build new image
(hgt1, wid1, dep1)= img1.shape
(hgt2, wid2, dep2)= img2.shape
newWid = wid1 + wid2
newHgt = max(hgt1, hgt2)
hgtDiff = abs(hgt1 - hgt2) / 2
newImage = numpy.zeros((newHgt, newWid, 3), numpy.uint8)
newImage[0:hgt2, 0:wid2] = img2
newImage[0:hgt1, wid2:wid1+wid2] = img1


# draw lines for matches
for m in goodMatches:
    kp_a = keypts1[m.queryIdx].pt
    intKpA = ( int(kp_a[0]) + wid2, int(kp_a[1]) )
    kp_b = keypts2[m.trainIdx].pt
    intKpB = ( int(kp_b[0]), int(kp_b[1]) )
    cv2.line(newImage, intKpA, intKpB, (255, 0, 0))
    cv2.imshow("Combined", newImage)


cv2.waitKey(0)
