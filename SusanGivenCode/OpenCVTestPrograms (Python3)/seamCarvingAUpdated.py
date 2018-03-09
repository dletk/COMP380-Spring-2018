

import cv2
import random
import numpy as np


def computeSobel(image):
    """Takes in an RGB color image and computes the Sobel value for it. The
    grayscale Sobel "energy" image is the value returned."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Compute gradient in horizontal direction (detects vertical edges)
    sobelValsHorz = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
    horzImg = cv2.convertScaleAbs(sobelValsHorz)
    #cv2.imshow("horizontal gradient", horzImg)
    # Compute gradient in vertical direction (Detects horizontal edges)
    sobelValsVerts = cv2.Sobel(gray, cv2.CV_32F, 0, 1)
    vertImg = cv2.convertScaleAbs(sobelValsVerts)
    #cv2.imshow("vertical gradient", vertImg)
    # Combine the two gradients
    sobelComb = cv2.addWeighted(sobelValsHorz, 0.5,
                                sobelValsVerts, 0.5, 0)
    # Convert back to uint8
    sobelImg = cv2.convertScaleAbs(sobelComb)
    #cv2.imshow("Sobel", sobelImg)        
    #cv2.waitKey(0)
    return sobelImg




def verticalSeamFind(image):
    """Takes in a grayscale image and determines with dynamic programming the best
    path from top to bottom. Best path has lowest energy, thus least likely to be noticed."""
    (height, width) = image.shape
    # build a table that is the same size as the image: width by height
    # entries in the table will be dictionaries with keys 'data' and 'path'
    # 'data' holds the total energy of the best path to this point, and 'path'
    # holds the location of the neighbor in the previous row (-1, 0, or 1)
    energTable = image.astype(np.uint32)
    pathTable = np.zeros( (height, width), np.int_ )

    # These loops fill in the table, row by row from top to bottom.
    
    for r in range(1, height):
        leftRow = energTable[r-1, 0:width-2]
        midRow = energTable[r-1, 1:width-1]
        rightRow = energTable[r-1, 2:width]
        minRow = np.minimum( np.minimum(leftRow, midRow), rightRow )
        fromLeft = np.equal(leftRow, minRow)
        fromMid = np.logical_and(np.equal(midRow, minRow), 
                                 np.logical_not(fromLeft))
        fromRight = np.logical_and( np.logical_and( np.equal(rightRow, minRow), 
                                                    np.logical_not(fromMid) ),
                                    np.logical_not(fromLeft) )
        minEnergs = ((1 * fromLeft) + (2 * fromMid) + (3 * fromRight)) - 2
        pathTable[r, 1:width-1] = minEnergs
        energTable[r, 1:width-1] += minRow
        firstVal = min(energTable[r-1, 0], energTable[r-1, 1])
        energTable[r, 0] += firstVal 
        pathTable[r, 0] = int(firstVal == energTable[r-1, 1])
        lastVal = min(energTable[r-1, width-2], energTable[r-1, width-1])
        energTable[r, width-1] += lastVal
        pathTable[r, width-1] = int( lastVal == energTable[r-1, width - 1]) - 1  # adjust so values are -1 and 0, not 0 and 1
        
        
        
   # The next part finds the column in the final row of the table that has the smallest total cost
    minPos = np.argmin(energTable[height-1, :])
    minTotal = energTable[height-1, minPos]
   # Return the final path, reconstructed from the table
    return findVerticalSeam(minPos, pathTable, width, height), minTotal




def findVerticalSeam(startPos, table, width, height):
    """Takes in a start position and a table, and it builds the minimum energy path as a series of
    indices. Each index is a column position, and they correspond to the rows from the top of the image
    to the bottom."""
    row = height - 1
    currPos = startPos
    path = [startPos]
    while row >= 0:
        nextDir = int(table[row, currPos])
        currPos = currPos + nextDir
        path.append(currPos)
        row = row - 1
    return path[::-1]


def horizontalSeamFind(image):
    """Takes in a grayscale image and determines with dynamic programming the best
    path from left to right. Best path has lowest energy, thus least likely to be noticed."""
    newImg = cv2.transpose(image)
    return verticalSeamFind(newImg)



def drawPath(image, path, energy, color = (255, 0, 255), seamDir = 'v'):
    """Takes in a color image and a path (columns in order from first row to last), and
    an optional color argument, and it draws the seam on the image."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    if seamDir == 'v':
        drawVertPath(image, path, color)
    else:
        newImg = cv2.transpose(image)
        drawVertPath(newImg, path, color)
        image = cv2.transpose(newImg)
    cv2.putText(image, "Best Energy: " + str(energy), (path[0] + 10, 30),
                font, 0.75, (255, 0, 255))
    
    cv2.imshow("Seam", image)

        
def drawVertPath(image, path, color):
    for row in range(0, len(path) - 1):
        col1 = path[row]
        col2 = path[row+1]
        cv2.line(image, (col1, row), (col2, row+1), color, 1)


 


def removePath(image, path, seamDir):
    """Takes in an image, a path/seam, and whether that seam is horizontal or vertical, and it
    removes the seam, making an image that is one smaller in the given direction."""
    if seamDir == 'v':
        return removeVerticalPath(image, path)
    else:
        return removeHorizPath(image, path)
    
 
def removeVerticalPath(image, path):
    """Takes in an image and a vertical seam, and it removes the pixels
    that are indicated in the vertical seam/path. It returns a new image."""
    (height, width, depth) = image.shape
    newImg = np.zeros( (height, width-1, depth), np.uint8 )
    for row in range(height):
        col = path[row]
        newImg[row, 0:col] = image[row, 0:col]
        newImg[row, col:] = image[row, (col+1):]
    return newImg


def removeHorizPath(image, path):
    """Takes in an image and a horizontal seam, and it removes the pixels
    that are indicated in the horizontal seam/path. It returns a new image."""
    (height, width, depth) = image.shape
    newImg = np.zeros( (height-1, width, depth), np.uint8 )
    for col in range(width):
        row = path[col]
        newImg[0:row, col] = image[0:row, col]
        newImg[row:, col] = image[(row+1):, col]
    return newImg

def addPath(image, path, seamDir = 'v'):
    if seamDir == 'v':
        return addVerticalPath(image, path)
        
        
def addVerticalPath(image, path):
    """Takes in an image and a vertical seam, and it adds a new row next to the given
    seam, setting the colors to be the average of the seam's and the one to its right.
    It returns a new image."""
    (height, width, depth) = image.shape
    newImg = np.zeros( (height, width+1, depth), np.uint8 )
    for row in range(height):
        col = path[row]  
        newImg[row, 0:(col+1)] = image[row, 0:(col+1)]
        newImg[row, (col+2):] = image[row, (col+1):]
        #newImg[row, col+1,0:3] = cv2.addWeighted(image[row, col], 0.5, image[row, col+1], 0.5, 0)
        
        x = cv2.addWeighted(image[row, col,:], 0.5, image[row, col+1,:], 0.5, 0)
        print("x is", x)
        newImg[row, col+1, :] = x.reshape((1, 1, 3))
    return newImg


def doVideo(): 
    """Takes images from the camera and finds the seam in them."""
    
    cam = cv2.VideoCapture(0)
    
    while True:
        ret, image = cam.read()
        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        (height, width, depth) = image.shape
        cv2.imshow("Cam", image)
        visImg = image.copy()
        energyImg = computeSobel(image)
        path1, energy1 = verticalSeamFind(energyImg)
        #path2, energy2, bad1, badE1 = randomWalkPathFind(energyImg, 500)
        drawPath(visImg, path1, energy1, (255, 0, 255))   # magenta for dynamic programming method
        inp = cv2.waitKey(10)
        if inp != -1:
            if chr(inp) == 'q':
                break
            
            
    cv2.destroyAllWindows()
        



def doStill(filename, scaleFactor = 1.0): 
    """Takes images from the camera and finds the seam in them."""
    currMode = 'v'
    image = cv2.imread(filename)
    image = cv2.resize(image, (0, 0), fx = scaleFactor, fy = scaleFactor)
    (h, w, d) = image.shape
    cv2.namedWindow("Original Image")
    cv2.namedWindow("Cropped Image")
    cv2.namedWindow("Seam")
    cv2.moveWindow("Original Image", 50, 50)
    cv2.moveWindow("Cropped Image", 50 + w + 10, 50)
    cv2.moveWindow("Seam", 50 + w + 10, 50 + h + 10)
    #image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    origImage = image.copy()
    cv2.imshow("Original Image", origImage)
    cv2.waitKey(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    (height, width, depth) = image.shape
    fileNum = 0
    while True:
        cv2.imshow("Cropped Image", image)
        visImg = image.copy()
        energyImg = computeSobel(image)
        if currMode == 'v':
            path, energy = verticalSeamFind(energyImg)
        else:
            path, energy = horizontalSeamFind(energyImg)
        drawPath(visImg, path, energy, (255, 0, 255), currMode)   # magenta for dynamic programming method

        nextImg = removePath(image, path, currMode)
        #nextImg = addPath(image, path, currMode)
        
        image = nextImg

        inp = cv2.waitKey(0)
        if inp != -1:
            if chr(inp) == 'q':
                break
            elif chr(inp) == 'v':
                currMode = 'v'
            elif chr(inp) == 'h':
                currMode = 'h'
            elif chr(inp) == 's':
                cv2.imwrite("CroppedIm" + str(fileNum) + ".jpg", image)
                cv2.imwrite("WithSeams" + str(fileNum) + ".jpg", visImg)
                fileNum += 1
            
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
        

doStill("../TestImages/grandTetons.jpg") 
#doStill("../TestImages/Landscape1.jpg", 0.3)
#doVideo()



def randomWalkPathFind(image, nReps = 1000):
    """Takes in a grayscale image and finds the best among nReps random paths
    from top to bottom. You can change nReps from the default 1000 to some
    input amount. Returns the path."""
    (height, width) = image.shape
    bestPath = None             # keep track of the lowest-energy path generated so far
    bestEnergy = None
    worstPath = None
    worstEnergy = None
    for rep in range(nReps):
        path, energy = doRandomWalk(image, width, height)  # generates a single path from first row to last
        if bestEnergy == None or bestEnergy > energy:
            bestPath = path
            bestEnergy = energy
        if worstEnergy == None or worstEnergy < energy:
            worstPath = path
            worstEnergy = energy
    return bestPath, bestEnergy, worstPath, worstEnergy
        
        
        
def doRandomWalk(image, width, height):
    """Takes in a grayscale energy image, and the images width and height, and it randomly generates
    a seam from first row to last, always using adjacent pixels. Returns the seam and its total energy
    as the result."""
    currPos = random.randrange(width)
    path = [currPos]
    totalEnergy = int(image[0][currPos])
    for i in range(1, height):
        if currPos == 0:
            nextStep = random.choice([0, 1])
        elif currPos == width - 1:
            nextStep = random.choice([-1, 0])
        else:
            nextStep = random.choice([-1, 0, 1])
        currPos = currPos + nextStep
        path.append(currPos)
        totalEnergy += int(image[i][currPos])
    return path, totalEnergy

