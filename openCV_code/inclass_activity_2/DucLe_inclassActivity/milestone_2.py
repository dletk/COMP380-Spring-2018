import cv2
import numpy as np

# Select 2 image to blend
img1 = cv2.imread("../TestImages/fallWoods.jpg")
img2 = cv2.imread("../TestImages/beachBahamas.jpg")

(height1, width1, depth) = img1.shape
(height2, width2, depth) = img2.shape

height = min(height1, height2)
width = min(width1, width2)

# Crop the img1 and img2 to the same size before blending
img1 = img1[0:height, 0:width]
img2 = img2[0:height, 0:width]

# Initial weight of each image in the blended image
weight1 = 0.5
weight2 = 0.5

while True:
    image_blended = cv2.addWeighted(img1, weight1, img2, weight2, 0)

    cv2.imshow("Image blended", image_blended)
    # Get the key pressed
    key_stroke = cv2.waitKey(0) & 0xff
    key_stroke = chr(key_stroke)

    # Make a little interface to increase the weight of img1 or img2, or quit
    if key_stroke == 'q':
        break
    elif key_stroke == 'a':
        weight1 += 0.1
        weight2 -= 0.1
    elif key_stroke == 'd':
        weight2 += 0.1
        weight1 -= 0.1
