import sys
import cv2
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="input video file name")
ap.add_argument("-c", type=int, help="number of classes")
ap.add_argument("-f", type=int, help="amount of frame to skip")
args = vars(ap.parse_args())

skip = args.get('f')
filename = args.get("video")[6:-4]
n_classes = args.get('c')

# Create a video capture object to read videos
cap = cv2.VideoCapture(args.get('video'))

WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
    print('Failed to read video')
    sys.exit(1)

## Select boxes
bboxes = []
classes = []
count = 0
currentClass = 0
# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
    # draw bounding boxes over objects
    # selectROI's default behaviour is to draw box starting from the center
    # when fromCenter is set to false, you can draw box starting from top left corner
    bbox = cv2.selectROI('MultiTracker', frame)
    print(bbox)
    if bbox == (0, 0, 0, 0):
        continue
    bboxes.append(bbox)
    print('Select bounding box class')
    sys.stdout.write('\rCurrent class: {}'.format(currentClass))
    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == ord('e'):
            currentClass += 1
            currentClass = currentClass % n_classes
            sys.stdout.write('\rCurrent class: {}'.format(currentClass))
        elif k == ord('q'):
            currentClass -= 1
            currentClass = currentClass % n_classes
            sys.stdout.write('\rCurrent class: {}'.format(currentClass))
        elif k == 13:  # enter is pressed
            print('\nChose class ', currentClass)
            classes.append(currentClass)
            break
    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")
    k = cv2.waitKey(0) & 0xFF
    if k == ord('q'):
        break

print('Selected bounding boxes {}'.format(bboxes))
print('Corresponding classes {}'.format(classes))

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker
for bbox in bboxes:
    multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)

# Process video and track objects
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)


    # draw tracked objects
    for i, newbox in enumerate(boxes):
        # p1 top left, p2 bottom right, dim width height, center coordinates.
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        dim = (int(newbox[2]), int(newbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 225))
        center = (p1[0] + dim[0] / 2, p1[1] + dim[1] / 2)
        if os.path.isdir('bbox_txt/'):
            if count % skip == 0:
                f = open('bbox_txt/' + filename + '_' + str(count) + '.txt', 'a+')
                f.write("{} {} {} {} {}\n".format(classes[i], center[0] / WIDTH, center[1] / HEIGHT, dim[0] / WIDTH,
                                                dim[1] / HEIGHT))
        else:
            os.mkdir('bbox_txt')
            if count % skip == 0:
                f = open('bbox_txt/' + filename + '_' + str(count) + '.txt', 'a+')
                f.write("{} {} {} {} {}\n".format(classes[i], center[0] / WIDTH, center[1] / HEIGHT, dim[0] / WIDTH,
                                                dim[1] / HEIGHT))
    count += 1
    # show frame
    cv2.imshow('MultiTracker', frame)

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
