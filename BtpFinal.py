import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam or input video file
if args.get("video", None) is None:
	camera = cv2.VideoCapture("ankit.MPG")
	time.sleep(0.25)

# otherwise, we are reading from a video file provide at terminal
else:
	print "path " , args["video"]
	camera = cv2.VideoCapture(args["video"])

print "path " , args["video"]
# initialize the first frame in the video stream
firstFrame = None
count=0

while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	#text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break
	
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	rows,columns,channels = frame.shape
	roww=(2*rows)/3
	cv2.line(frame,(0,roww),(columns-1,roww),(255,0,0),1)
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	_,contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	
	
	
	for c in contours:
		#print "area " , args["min_area"]
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		
		x1 = w/2
		y1 = h/2
		cx = x + x1
		cy = y + y1
		centroid = (cx,cy)
		cv2.circle(frame,(int(cx),int(cy)),2,(0,255,0),-1)
		
		if(cy<roww+1.5 and cy>roww-1.5):
			if(h>248):
				count=count+2  
				print ' count = ', count
				print 'height  ', h
				print 'weight  ', w
			else:
				count=count+1 
				print ' count = ', count
				print 'height  ', h
				print 'weight  ', w
		cv2.putText(frame, "Count : {}".format(count), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		
	# show the frame and record if the user presses a key
	cv2.imshow("Thresh", thresh)
	cv2.imshow("People Counter", frame)
	
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	
		
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break		

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


