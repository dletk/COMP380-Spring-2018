import cv2

# Create the video capture object
videoCap = cv2.VideoCapture(0)

# Ask for user's option
userOption = input("Would you want to record [r] or capture [c]: ")
record = userOption == "r"
capture = userOption == "c"

# Case 1: Recording a short video
if record:
    # Only begin the recording when user is ready
    print("Select the window and hit [b] to begin recording.")
    retVal, frame = videoCap.read()

    # Get the size of the video frame
    size = (int(videoCap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # Create the writer to save the recorded video
    videoWriter = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, size)

    # Show the current frame so user knows that it is working
    cv2.imshow("Video", frame)

    # While user has not yet pressed 'b', do not continue the program
    while True:
        key = cv2.waitKey(1) & 0xFF
        if chr(key) == 'b':
            break

    # Continue displaying the video while there is more frame
    while retVal:
        # Get the current frame
        retVal, frame = videoCap.read()
        # Show the current frame
        cv2.imshow("Video", frame)
        # Save the current frame to recorded file
        videoWriter.write(frame)

        # Check whether the 'quit' option is pressed
        keyChar = cv2.waitKey(1)
        keyChar = keyChar & 0xFF
        if chr(keyChar) == 'q':
            videoCap.release()
            videoWriter.release()
            cv2.destroyAllWindows()
            break
elif capture:
    retVal, frame = videoCap.read()
    while retVal:
        cv2.imshow("Video", frame)
        keyChar = cv2.waitKey(1)
        keyChar = keyChar & 0xFF
        if chr(keyChar) == 'q':
            videoCap.release()
            cv2.destroyAllWindows()
            break
        elif chr(keyChar) == 'c':
            cv2.imwrite("outputImage.jpg", frame)
        retVal, frame = videoCap.read()
