from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from new_outdoor_strategies_v1_0_0 import getObjectsInImage

def Vision():
	"""
	Initialize the camera and grab a reference to the raw camera capture
	"""
	camera = PiCamera()
	rawCapture = PiRGBArray(camera)
	# allow the camera to warmup
	time.sleep(0.1)
	# grab an image from the camera
	camera.capture(rawCapture, format="bgr")

	image = rawCapture.array
	[img_detected, distanceBallYellow, distanceBallRed, distanceBallBlue, distanceGoalYellow, distanceGoalRed, distanceGoalBlue, 
	angleGoalYellow, angleGoalRed, 
	angleGoalBlue, angleBallYellow, angleBallRed, angleBallBlue] = getObjectsInImage(image)
	camera.close()	
	return [distanceBallYellow, distanceBallRed, distanceBallBlue, distanceGoalYellow, distanceGoalRed, distanceGoalBlue, 
	angleGoalYellow, angleGoalRed, 
	angleGoalBlue, angleBallYellow, angleBallRed, angleBallBlue]

	# If needed to validate the images
	#cv2.imshow("Image", img_detected)
	#cv2.imwrite("20cm.jpg", img_detected)
	#cv2.waitKey(0)

