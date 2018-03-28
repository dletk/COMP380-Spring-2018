import cv2
img = cv2.imread("../TestImages/shops.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Compute gradient in horizontal direction (detects vertical edges)
sobelValsHorz = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
horzImg = cv2.convertScaleAbs(sobelValsHorz)
cv2.imshow("horizontal gradient", horzImg)

# Compute gradient in vertical direction (Detects horizontal edges)
sobelValsVerts = cv2.Sobel(gray, cv2.CV_32F, 0, 1)
vertImg = cv2.convertScaleAbs(sobelValsVerts)
cv2.imshow("vertical gradient", vertImg)

# Combine the two gradients
sobelComb = cv2.addWeighted(sobelValsHorz, 0.5,
                            sobelValsVerts, 0.5, 0)
# Convert back to uint8
sobelImg = cv2.convertScaleAbs(sobelComb)
cv2.imshow("Sobel", sobelImg)

cv2.waitKey(0)
