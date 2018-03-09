
import cv2
import numpy as np



def scaleDemo(img1, img2):
    """Take in two pictures, and demonstrate the resize function and some of its options."""
    for scale in [0.25, 0.5, 1.75, 2]:
        newImg = cv2.resize(img1, (0, 0), fx=scale, fy=scale)
        cv2.imshow("Scaled", newImg)
        cv2.waitKey()
    for wid, hgt in [(450, 450), (400, 800), (800, 400), (800, 100)]:
        newImg = cv2.resize(img2, (wid, hgt))
        cv2.imshow("Scaled", newImg)
        cv2.waitKey()




def translateDemo(img):
    """Take in a picture and show how translation works"""
    cv2.imshow("Original", img)
    (hgt, wid, dep) = img.shape
    for (xDist, yDist) in [(50, 50), (50, 200), (-10, 50), (-50, -50)]:
        transMatrix = np.float32([[1, 0, xDist], [0, 1, yDist]])
        newIm = cv2.warpAffine(img, transMatrix, (2*wid, 2*hgt))
        cv2.imshow("Translated", newIm)
        cv2.waitKey()

    newIm = img.copy()
    for (xDist, yDist) in [(50, 50), (50, 200), (-10, 50), (-50, -50)]:
        transMatrix = np.float32([[1, 0, xDist], [0, 1, yDist]])
        newIm = cv2.warpAffine(newIm, transMatrix, (wid, hgt))
        cv2.imshow("Translated", newIm)
        cv2.waitKey()





def rotateDemo(img):
    """Takes in an image and uses it to show how to rotate an image."""
    cv2.imshow("Original", img)
    (hgt, wid, dep) = img.shape
    midPt = (wid / 2, hgt / 2)
    for angle in range(10, 180, 20):
        rotMat = cv2.getRotationMatrix2D(midPt, angle, 1)
        newIm = cv2.warpAffine(img, rotMat, (wid, hgt))
        cv2.imshow("Rotated", newIm)
        cv2.waitKey()

    for angle in range(10, 180, 20):
        rotMat = cv2.getRotationMatrix2D((0, 0), angle, 1)
        newIm = cv2.warpAffine(img, rotMat, (2 * wid, 2 * hgt))
        cv2.imshow("Rotated", newIm)
        cv2.waitKey()




def affineDemo(img):
    """Takes in an image and shows two general affine warps"""
    cv2.imshow("Original", img)
    (hgt, wid, dep) = img.shape
    print (wid, hgt)
    srcPoints = np.float32(((0, 0), (wid-1, 0), (0, hgt-1)))
    dstPoints = np.float32(((0, 300), (610, 0), (700, hgt-1)))
    warpMatrix = cv2.getAffineTransform(srcPoints, dstPoints)
    newIm = cv2.warpAffine(img, warpMatrix, (wid, hgt))
    cv2.imshow("Warp Affine", newIm)
    cv2.waitKey()

    srcPoints = np.float32(((50, 50), (500, 300), (80, 370)))
    dstPoints = np.float32(((10, 10), (520, 10), (30, hgt-20)))
    warpMatrix = cv2.getAffineTransform(srcPoints, dstPoints)
    newIm = cv2.warpAffine(img, warpMatrix, (wid, hgt))
    cv2.imshow("Warp Affine", newIm)
    cv2.waitKey()


def perspectiveDemo(img):
    """Takes in an image and shows two general affine warps"""
    cv2.imshow("Original", img)
    (hgt, wid, dep) = img.shape
    print (wid, hgt)
    srcPoints = np.float32(((0, 0), (wid-1, 0), (0, hgt-1), (wid-1, hgt-1)))
    dstPoints = np.float32(((0, 300), (610, 0), (700, hgt-1), (wid-1, 350)))
    warpMatrix = cv2.getPerspectiveTransform(srcPoints, dstPoints)
    newIm = cv2.warpPerspective(img, warpMatrix, (wid, hgt))
    cv2.imshow("Warp Perspective", newIm)
    cv2.waitKey()

    srcPoints = np.float32(((50, 50), (500, 300), (80, 370), (420, 550)))
    dstPoints = np.float32(((10, 10), (520, 10), (30, hgt-20), (522, hgt-40)))
    warpMatrix = cv2.getPerspectiveTransform(srcPoints, dstPoints)
    newIm = cv2.warpPerspective(img, warpMatrix, (wid, hgt))
    cv2.imshow("Warp Perspective", newIm)
    cv2.waitKey()




beach = cv2.imread("TestImages/beachBahamas.jpg")
mountain = cv2.imread("TestImages/Landscape1MuchSmaller.jpg")


# scaleDemo(beach, mountain)
# translateDemo(beach)
rotateDemo(mountain)
affineDemo(beach)
perspectiveDemo(beach)


cv2.destroyAllWindows()