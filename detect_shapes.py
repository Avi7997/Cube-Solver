# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])


height, width = resized.shape[:2]
print width
print height

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)


thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('Binary Threshold', thresh)

th2 = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
cv2.imshow('Adaptive Threshold', th2)

edges = cv2.Canny(resized,100,200)
cv2.imshow('Edges', edges)

# find contours in the thresholded image and initialize the
# shape detector


cnts = cv2.findContours(th2.copy(), cv2.RETR_LIST,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

sd = ShapeDetector()
cl = ColorLabeler()

# loop over the contours
cnt = 0

for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	#cX = int((M["m10"] / M["m00"]) * ratio)
	#cY = int((M["m01"] / M["m00"]) * ratio)
	
	shape = sd.detect(c, height)
	color = cl.label(lab, c)
	
	if shape=="square":
		cnt = cnt +1
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
		cv2.drawContours(resized, [c], -1, (0, 255, 0), 3)
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		
		#cv2.drawContours(image, [c], 0, (255,0, 0), 1)
		#cv2.drawContours(image, [c], 1, (0, 255, 255), 2)
		#cv2.drawContours(image, [c], 2, (255, 255, 0), 2)
		
		text = "{} {}".format(color, shape)
		print text
		
		
	#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	0.5, (255, 255, 255), 2)
	
	# show the output images
print cnt
cv2.imshow("Image", resized)
cv2.waitKey(0)