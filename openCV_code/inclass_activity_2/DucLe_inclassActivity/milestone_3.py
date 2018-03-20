import cv2
import numpy as np

original_image = cv2.imread("../TestImages/beachBahamas.jpg")
(rows, cols, depth) = original_image.shape
cv2.imshow("Original image", original_image)


def translation():
    x_trans = 0
    y_trans = 0
    trans_amount = 3

    while True:
        translation_matrix = np.float32([[1, 0, x_trans], [0, 1, y_trans]])
        translated_image = cv2.warpAffine(
            original_image, translation_matrix, (cols, rows))

        cv2.imshow("Translated image", translated_image)

        key_stroke = cv2.waitKey(0) & 0xff
        key_stroke = chr(key_stroke)

        if key_stroke == 'q':
            break
        elif key_stroke == 'w':
            y_trans -= trans_amount
        elif key_stroke == 's':
            y_trans += trans_amount
        elif key_stroke == 'a':
            x_trans -= trans_amount
        elif key_stroke == 'd':
            x_trans += trans_amount


def rotation():
    rotation_degree = 30.0
    while True:
        # Get the rotation matrix with center is the center of the image
        rotationMatrix = cv2.getRotationMatrix2D(
            (cols // 2, rows // 2), rotation_degree, 1)

        rotated_image = cv2.warpAffine(
            original_image, rotationMatrix, (cols, rows))

        cv2.imshow("Rotated image", rotated_image)

        key_stroke = chr(cv2.waitKey(0) & 0xff)
        if key_stroke == 'l':
            rotation_degree -= 5
        elif key_stroke == 'r':
            rotation_degree += 5
        elif key_stroke == 'q':
            break


def generalWarp():
    origPoints = np.float32([[40, 40], [160, 40], [40, 160]])
    newPoints = np.float32([[10, 80], [180, 5], [35, 193]])
    mat = cv2.getAffineTransform(origPoints, newPoints)
    new_image = cv2.warpAffine(original_image, mat, (cols, rows))

    cv2.imshow("Warped image", new_image)

    cv2.waitKey(0)


translation()
# rotation()
# generalWarp()
