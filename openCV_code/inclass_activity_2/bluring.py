import cv2
import numpy as np

original_image = cv2.imread("../TestImages/beachBahamas.jpg")

width = 1
height = 1
blur_mode = 1

while True:
    kerner_size = (width, height)

    if blur_mode == 1:
        blur_image = cv2.blur(original_image, kerner_size)
        txt_display = "Blurred image with kernel size width=" + \
            str(width) + " and height=" + str(height)
    elif blur_mode == 2:
        blur_image = cv2.GaussianBlur(original_image, kerner_size, 0)
        txt_display = "Gaussian Blurred image with kernel size width=" + \
            str(width) + " and height=" + str(height)

    blur_image = cv2.putText(blur_image, txt_display, (5, 20),
                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0))

    cv2.imshow("Original image", original_image)
    cv2.imshow("Blurred image", blur_image)

    key_stroke = chr(cv2.waitKey(0) & 0xff)

    if key_stroke == 'a':
        width = width - 2 if width > 1 else 1
    elif key_stroke == 'd':
        width += 2
    elif key_stroke == 'w':
        height += 2
    elif key_stroke == 's':
        height = height - 2 if height > 1 else 1
    elif key_stroke == '1':
        blur_mode = 1
    elif key_stroke == '2':
        blur_mode = 2
    elif key_stroke == 'q':
        break
