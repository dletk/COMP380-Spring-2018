import cv2

image1 = cv2.imread("TestImages/SnowLeo1.jpg")
if image1 is None:
    print("Error reading image")
else:
    window = cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("image", image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
