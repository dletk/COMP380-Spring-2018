import cv2
import os

path = "./TestImages/"

# Get all the image file names from the folder TestImages
list_files = [file_name for file_name in os.listdir(path=path)
              if file_name.endswith(".jpg")]

window = cv2.namedWindow("Image window", cv2.WINDOW_AUTOSIZE)

for image_name in list_files:
    image = cv2.imread(path + image_name, cv2.IMREAD_UNCHANGED)
    if image is None:
        print("Error reading image")
    else:
        cv2.imshow("Image window", image)
        cv2.waitKey(1000)
