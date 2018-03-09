import cv2
import numpy

img1 = cv2.imread("TestImages/SnowLeo2.jpg")
cv2.imshow("SnowGuy Original", img1)
        

kWid = 3
kHgt = 3
whichBlur = 1

while True:
    if whichBlur == 1:
        blurImg = cv2.blur(img1, (kWid, kHgt))
        descrString = "Plain blur width = " + str(kWid) + ", height = " + str(kHgt)
    else:
        blurImg = cv2.GaussianBlur(img1, (kWid, kHgt), 0)
        descrString = "Gauss blur width = " + str(kWid) + ", height = " + str(kHgt)
        
    cv2.putText(blurImg, descrString, (5, 15), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
    cv2.imshow("Blurred Image", blurImg)    
    code = cv2.waitKey(0)
    char = chr(code & 0xFF)
    if char == 'q':
        break
    elif char == 'w':
        kHgt += 2
    elif char == 's':
        kHgt -= 2
        if kHgt < 1:
            kHgt = 1
    elif char == 'a':
        kWid -= 2
        if kWid < 1:
            kWid = 1
    elif char == 'd':
        kWid += 2
    elif char == '1':
        whichBlur = 1
    elif char == '2':
        whichBlur = 2


cv2.destroyAllWindows()
