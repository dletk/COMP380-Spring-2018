import cv2
import time

videoCap = cv2.VideoCapture(0)
window = cv2.namedWindow("Webcam", cv2.WINDOW_AUTOSIZE)

begin = time.time()
for i in range(300):
    ret, image = videoCap.read()
    cv2.imshow("Webcam", image)
    cv2.waitKey(1)
print(time.time() - begin)

cv2.destroyAllWindows()
videoCap.release()
