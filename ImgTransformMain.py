# necessary packages
from ImgTransformFunc import four_point_transform
import numpy as np 
import argparse 
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",help = "path to the image file")
ap.add_argument("-c", "--coords", help = "comma seperated list of \
	source points")
args = vars(ap.parse_args())

# load the img and grab the source coordinates (i.e the list 
# of (x,y) points)
#
# NOTE TO SELF
# usually dnt use eval find something better
img = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), np.float32)

# apply the four point transform to obtain birds eye view 
# of img
warped = four_point_transform(image,pts)

# show original and warped
cv2.imshow("original", image)
cv2.imshow("warped",warped)
cv2.waitKey(0)
cv2.destoryAllWindows()

