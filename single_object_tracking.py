from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="input video file name")
ap.add_argument("-c", type=int, help="item class")
ap.add_argument("-f", type=int, help="amount of frame to skip")
args = vars(ap.parse_args())

skip = args.get("f")
filename = args.get("video")[7:13]
tracker = cv2.TrackerKCF_create()

# initialize the bounding box coordinates of the object we are tracking
initBB = None

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args.get("video"))

WIDTH = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

count = 0

# loop over frames from the video stream
while True:
	# grab the current frame
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame

	# check to see if we have reached the end of the stream
	if frame is None:
		break

	# resize the frame so we can process it faster
	frame = imutils.resize(frame, width=1080)

	# check to see if we are currently tracking an object
	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)

		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
			center = ((x+w/2)/WIDTH, (y+h/2)/HEIGHT)
			dim = (w/WIDTH, h/HEIGHT)
			if os.path.isdir('bbox/'):
				if count%skip==0:
					f = open('bbox/'+filename+'_'+str(count)+'.txt', 'w+')
					f.write("{} {} {} {} {}".format(args["c"], center[0], center[1], dim[0], dim[1]))
					print("center:", center, " dim: ", dim," class: ", args["c"])
			else:
				os.mkdir('bbox')

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	count += 1
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)

		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)
		fps = FPS().start()

	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()