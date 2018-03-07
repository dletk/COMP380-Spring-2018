import cv2
import os
import random

path = "./TestImages/"

list_files = [file_name for file_name in os.listdir(path=path) if file_name.endswith(".jpg")]

# Creat the window to display all four images
window = cv2.namedWindow("Image window", cv2.WINDOW_AUTOSIZE)

for i in range(4):
    image = cv2.imread(path + random.choice(list_files))
    if image is None:
        print("Error while reading image")
    else:
        cv2.imshow("Image window", image)
        cv2.waitKey(0)
