import cv2
import numpy as np


def calculateAbsDifference(img1, img2, img3):
    diff1 = cv2.absdiff(img2, img1)
    diff2 = cv2.absdiff(img2, img3)
    return cv2.bitwise_and(diff1, diff2)


def calculateAbsDiff(img1, img2):
    return cv2.absdiff(img1, img2)


if __name__ == '__main__':
    videoCap = cv2.VideoCapture(0)

    ret, frame = videoCap.read()
    ret, frame2 = videoCap.read()
    # ret, frame3 = videoCap.read()

    while ret:
        # difference_image = calculateAbsDifference(frame, frame2, frame3)
        difference_image = calculateAbsDiff(frame, frame2)

        enhanced_edges_image = cv2.morphologyEx(
            difference_image, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)))

        enhanced_edges_image = cv2.GaussianBlur(
            enhanced_edges_image, (9, 9), 0)

        gray_image = cv2.cvtColor(enhanced_edges_image, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray_image, 5, 255, cv2.THRESH_BINARY)

        # Erosion to eliminate too small contours
        erode_kernel = (3,3)
        eroded_image = cv2.erode(thresh, erode_kernel, iterations=5)
        # Dilation to connect the close contor
        # Loop several time
        dilated_kernel = (500, 500)
        # dilated_image = cv2.dilate(thresh, dilated_kernel)
        # for i in range(20):
        dilated_image = cv2.dilate(eroded_image, dilated_kernel, iterations=20)

        image, contours, hier = cv2.findContours(
            dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print("===> VIDEO CONTOURS: ", len(contours))
        # result_image = cv2.drawContours(
        #     frame2, contours, -1, (0, 255, 0))

        # Drawing the rectanle around the contours
        for contour in contours:
            (x, y, width, height) = cv2.boundingRect(contour)
            # print("====> RECT: ", (x, y, width, height))
            cv2.rectangle(frame2, (x, y),
                          (x + width, y + height), (255, 0, 0), 2)

        cv2.imshow("Video", frame2)

        # Create an image for quick comparison
        # image, contours, hier = cv2.findContours(
        #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # compare_image = cv2.drawContours(
        #     thresh, contours, -1, (0, 255, 0))
        # cv2.imshow("Compare", compare_image)
        # print("COMPARE CONTOURS: ", len(contours))

        key_stroke = chr(cv2.waitKey(1) & 0xff)

        if key_stroke == "q":
            break
        else:
            ret, frame = videoCap.read()
            # frame2 = frame3
            ret, frame2 = videoCap.read()
