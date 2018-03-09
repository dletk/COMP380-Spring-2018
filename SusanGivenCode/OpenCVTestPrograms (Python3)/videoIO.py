

import cv2

# ====================================================================
# This portion reads from an AVI file

def playVideo(filename):
    """Takes in a string, a filename (AVI) and plays the video."""
    cap = cv2.VideoCapture(filename)  
    ch = ' '
    r, frame = cap.read()
    cv2.imshow("Video", frame)
    cv2.waitKey(0)
    while r == True and ch != 'q':
        cv2.imshow("Video", frame)
        x = cv2.waitKey(30)
        ch = chr(x & 0xFF)
        r, frame = cap.read()
    
    cap.release()
    cv2.destroyAllWindows()


# ====================================================================
# This portion writes two an AVI file

def saveVideo(filename, cameraNum):
    cap = cv2.VideoCapture(cameraNum)
    r, f = cap.read()
    cv2.imshow("Video", f)
    cv2.waitKey(0)
    wid = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hgt = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(wid), int(hgt))
    #print(size)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    #print(fourcc)
    writ = cv2.VideoWriter(filename, fourcc, 25.0, size, 1)

    while cap.isOpened():
        r, f= cap.read()
        if r:
            writ.write(f)
            cv2.imshow("Video", f)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap.release()
    writ.release()
    cv2.destroyAllWindows()

def getUserInput(text, validInputs = []):
    while True:
        inp = input(text)
        if inp in validInputs or validInputs == []:
            return inp

if __name__ == '__main__':
    print("Notes:")
    print("    * Built for AVI files, others may be iffy")
    print("    * Both options show a still at first, type a key to start video")
    opt = getUserInput("Enter 1 to play a video, enter 2 to save a video from webcam: ", ["1", "2"])
    fName = getUserInput("Enter path and filename, including extension: ")
    if opt == "1":
        playVideo(fName)
    else:
        whichCamera = getUserInput("Use built-in camera [b] or auxiliary camera [a]: ", ['b', 'a'])
        if whichCamera == 'b':
            cameraNum = 0
        else:
            cameraNum = 1
        saveVideo(fName, cameraNum)
        
