import cv2
import numpy as np

def calculateAbsDiff(img1, img2):
    return cv2.absdiff(img1, img2)

if __name__ == '__main__':
    # Using the external webcam
    videoCap = cv2.VideoCapture(1)

    # Capture 2 continuous frames from the webcam to measure differences
    ret, frame = videoCap.read()
    ret, frame2 = videoCap.read()

    while ret:
        # Calculate the differences between 2 frames
        difference_image = calculateAbsDiff(frame, frame2)
        frame = frame2.copy()

        # Enhanced the edges in the images
        enhanced_edges_image = cv2.morphologyEx(
            difference_image, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)))

        # Blur out some negligible details
        enhanced_edges_image = cv2.GaussianBlur(
            enhanced_edges_image, (5, 5), 0)

        # Convert the image to proper format for finding contours
        gray_image = cv2.cvtColor(enhanced_edges_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 5, 255, cv2.THRESH_BINARY)


        # Dilation and erosion to eliminate too small contours and connect related
        # contours together. Interate several times to strengthen the effect.
        dilated_kernel = (10, 10)
        dilated_image = cv2.dilate(thresh, dilated_kernel, iterations=10)

        erode_kernel = (5,5)
        eroded_image = cv2.erode(dilated_image, erode_kernel, iterations=10)

        # Find all contours in the image
        image, contours, hier = cv2.findContours(
            eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Uncommented this to draw all contours
        # resulted_image = cv2.drawContours(frame2, contours, -1, (0,255,0))

        # Drawing the rectanle around the contours
        for contour in contours:
            (x, y, width, height) = cv2.boundingRect(contour)
            # If the boundingRect is too small, just ignore that area
            if width > 100 or height > 100:
                cv2.rectangle(frame2, (x, y),
                              (x + width, y + height), (255, 0, 0), 2)

        cv2.imshow("Video", frame2)

        key_stroke = chr(cv2.waitKey(1) & 0xff)
        if key_stroke == "q":
            break
        else:
            # ret, frame = videoCap.read()
            ret, frame2 = videoCap.read()
