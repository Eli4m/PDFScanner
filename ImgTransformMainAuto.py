from ImgTransformFunc import four_point_transform
import numpy as np
import argparse
import cv2
import imutils

# fix to import an image with its name 
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", requierd = True,help = "Path to the image to be scanned")
#args = vars(ap.parse_args())

 
# load image and compute the ratio of the old height
# to the new height clone it and resize

## fix this later
### image = cv2.imread(args["image"])

img = cv2.imread("../images/drawing.jpg")
ratio = img.shape[0]/500.0
orig = img.copy()
#resize to 500px to make the processing faster
img = imutils.resize(img,height = 500)

# convert the img to grayscale, blur it and find edges in the img
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
edge = cv2.Canny(gray,100,240)

# show the original image and the edge detected img
cv2.imshow("Image", img)
cv2.imshow("Edge",edge)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edge image keeping only the
# largest ones and initalize the screen contour
cnts = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts,key = cv2.contourArea, reverse = True)[:5]

# loop over contours
for c in cnts:
    # approximate the contour
    # loop up arcLength
    peri = cv2.arcLength(c,True)
    # look up approxPolyDp
    approx = cv2.approxPolyDP(c,0.02 * peri, True)

    # if out approximated contour has four points then we can assume that
    # we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the contour (outline) of the piece of paper
cv2.drawContours(img,[screenCnt],-1,(0,255,0),2)
cv2.imshow("Outline",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top down view of the og image
warped = four_point_transform(orig, screenCnt.reshape(4,2) * ratio)


kernel = np.ones((1,1),np.uint8)
warped = cv2.dilate(warped,kernel, iterations = 1)
warped = cv2.bitwise_not(warped)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(warped,15,40)
cv2.imshow("Canny",canny)

#removing noise
#warped = cv2.bilateralFilter(warped,9,75,75)

# show the og and scanned img
cv2.imshow("Original", imutils.resize(orig, height = 450))
cv2.imshow("Warpped",imutils.resize(warped, height = 450))
cv2.waitKey(0)
cv2.destroyAllWindows()
