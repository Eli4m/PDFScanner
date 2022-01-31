import numpy as np
import cv2
# SIDE NOTES
#-----------
# ROI region of intrest
# ** Performs exponential (power) calculation on operators 
# argmin returns min val along given axis
# argmax returns min val along given axis
#-----------
def order_points(pts):
	#initalize list of coordinates that will be orderd
	#such that the first entry of the list is the top left
	# the second is top right and thrid is bottom right 
	# and fourth finally bottom left
	rect = np.zeros((4,2), dtype = "float32")

	# the top left point has the smallest sum, whereas 
	# bottom right point will have largest sum
	

	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# compute diffrence between the points 
	# the top right point will have smallest diffrence
	# whereas the bottom left will have the largest dif
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# return the orderd coordinates
	return rect

def four_point_transform(image,pts):

	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	# tl = top left, tr = top right
	# br = bottom right, bl = bottom left
	(tl,tr,br,bl) = rect

	# compute width of the new image, which will be the max dist
	# between br and bl x-coordinates or the tr and tl x coordinates

	wA = np.sqrt(((br[0]-bl[0])**2) + ((br[1]-bl[1])**2))
	wB = np.sqrt(((tr[0]-tl[0])**2) + ((tr[1]-tl[1])**2))
	maxWidth = max(int(wA),int(wB))

	# compute the height of the new image which will be the 
	# maximum dist between tr and br y-coordinates
	# or the tl and bl y-coordinates
	hA = np.sqrt(((tr[0]-br[0])**2) + ((tr[1]-br[1])**2))
	hB = np.sqrt(((tl[0]-bl[0])**2) + ((tl[1]-bl[1])**2))
	maxHeight = max(int(hA), int(hB))

	# now that we have the dimensions of the new img
	# construct the set of destinationp oints to obtain
	# the birds eye view (top down) of the image, again
	# specifying points in the tl, tr, br and bl order
	
	# [0, 0] - top left corner 
	# [maxWidth - 1, 0] - top right corner 
	# [maxWidth - 1, maxHeight - 1] - bottom right corner
	# [0, maxHeight - 1] - bottom left corner 
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")


	#compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect,dst)
	warped = cv2.warpPerspective(image,M,(maxWidth,maxHeight))

	# return the warped image
	return warped
