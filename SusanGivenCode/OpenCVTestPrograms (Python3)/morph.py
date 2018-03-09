import numpy as np
import cv2


def update(dummy=None):
    """This is a callback function for the trackbar. Whenever either of the
    trackbars is moved, this function is called to update the status and create
    the new picture"""
    size = cv2.getTrackbarPos('operation size', 'morphology')
    iters = cv2.getTrackbarPos('iters', 'morphology')
    if len(currOpMode) > 1:
        size = size - 10
        if size > 0:
            op = currOpMode[1]
        else:
            op = currOpMode[0]
        size = abs(size)
    else:
        op = currOpMode[0]
   
    size = 2 * size + 1

    structElem = whichStructElem(currStructMode)
    operName = whichOper(op)
    st = cv2.getStructuringElement(structElem, (size,size))
    res = cv2.morphologyEx(img, operName, st, iterations=iters)
   
    cv2.putText(res,  'mode: ' + "/".join(currOpMode), (10, 20),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.putText(res, 'operation: ' + op, (10, 40), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.putText(res, 'structure: ' + currStructMode, (10, 60), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.putText(res, 'ksize: %d  iters: %d' % (size, iters), (10, 80), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.imshow('morphology', res)

def whichStructElem(structMode):
    structElems = {'ellipse': cv2.MORPH_ELLIPSE, 
                   'rect': cv2.MORPH_RECT, 
                   'cross': cv2.MORPH_CROSS}
    return structElems[structMode]

def whichOper(op):
    operations = {'erode': cv2.MORPH_ERODE,
                  'dilate': cv2.MORPH_DILATE,
                  'open': cv2.MORPH_OPEN,
                  'close': cv2.MORPH_CLOSE,
                  'blackhat': cv2.MORPH_BLACKHAT,
                  'tophat': cv2.MORPH_TOPHAT,
                  'gradient': cv2.MORPH_GRADIENT}
    return operations[op]


    
if __name__ == '__main__':
    fn = 'TestImages/SnowLeo2.jpg'
    img = cv2.imread(fn)

    modes = [('erode', 'dilate'), ('open', 'close'), ('blackhat', 'tophat'), ('gradient',)]
    modeIndex = 0
    structModes = ['ellipse', 'rect', 'cross']
    sModeIndex = 0
    
    currOpMode = modes[modeIndex]
    currStructMode = structModes[sModeIndex]

    cv2.namedWindow('morphology')
    cv2.createTrackbar('operation size', 'morphology', 12, 20, update)
    cv2.createTrackbar('iters', 'morphology', 1, 10, update)
    update()
    print("Controls:")
    print("  1 - change operation")
    print("  2 - change structure element shape")
    print()
    while True:
        code = cv2.waitKey()
        ch = chr(code & 0xFF)
        if ch == 'q': 
            break
        if ch == '1':
            modeIndex = (modeIndex + 1) % len(modes)
            currOpMode = modes[modeIndex]
        if ch == '2':
            sModeIndex = (sModeIndex + 1) % len(structModes)
            currStructMode = structModes[sModeIndex]
        update()
    cv2.destroyAllWindows()

