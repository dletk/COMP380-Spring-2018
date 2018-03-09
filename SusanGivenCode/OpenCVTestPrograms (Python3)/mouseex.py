import cv2
import numpy as np

startPt = None
endPt = None
dragging = False
img = None

# mouse callback function
def drawBox(event,x,y,flags,param):
    global startPt
    global currPt
    global endPt
    global dragging
    global img
    if (event == cv2.EVENT_LBUTTONDOWN) or (dragging == True and event == cv2.EVENT_MOUSEMOVE):
        if dragging == False:
            startPt = (x, y)
            dragging = True        
        endPt = (x, y)          
    if event == cv2.EVENT_LBUTTONUP:
        endPt = (x, y)
        dragging = False


# Create a black image, a window and bind the function to window

cap = cv2.VideoCapture(0)
cv2.namedWindow('Video')
cv2.setMouseCallback('Video',drawBox)

while(True):
    r, img = cap.read()
    dispImg = img.copy()
    if dragging == True:
        cv2.rectangle(dispImg, startPt, endPt, (255, 0, 0), 1)
    elif startPt != None and endPt != None:
        cv2.rectangle(dispImg, startPt, endPt, (255, 255, 0), 1)
    cv2.imshow("Video", dispImg)
        
    if dragging == False and startPt != None and endPt != None:
        minY = min(startPt[1], endPt[1])
        maxY = max(startPt[1], endPt[1])
        minX = min(startPt[0], endPt[0])
        maxX = max(startPt[0], endPt[0])
        roi = img[minY:maxY+1, minX:maxX+1]
        cv2.imshow("Selected part", roi)
    
    x = cv2.waitKey(20) & 0xFF
    if x == 27:
        break
    elif x == ord(' '):
        startPt = None
        endPt = None
        cv2.destroyWindow("Selected part")
    elif x == ord('s'):
        cv2.imwrite("saved.jpg", roi)
        startPt = None
        endPt = None
        cv2.destroyWindow("Selected part")
        

        
        
cap.release()    
cv2.destroyAllWindows()
