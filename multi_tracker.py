import sys
import cv2

tracker = cv2.TrackerKCF_create()

if __name__ == '__main__':
    # Set video to load
    videoPath = "videos/shelf1.mp4"

    # Create a video capture object to read videos
    cap = cv2.VideoCapture(videoPath)

    # Read first frame
    success, frame = cap.read()
    # quit if unable to read the video file
    if not success:
        print('Failed to read video')
        sys.exit(1)

    ## Select boxes
    bboxes = []

    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):  # q is pressed
            break

    print('Selected bounding boxes {}'.format(bboxes))

    ## Initialize MultiTracker
    # There are two ways you can initialize multitracker
    # 1. tracker = cv2.MultiTracker("CSRT")
    # All the trackers added to this multitracker
    # will use CSRT algorithm as default
    # 2. tracker = cv2.MultiTracker()
    # No default algorithm specified

    # Initialize MultiTracker with tracking algo
    # Specify tracker type

    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # Initialize MultiTracker
    for bbox in bboxes:
        multiTracker.add(tracker, frame, bbox)

    # Process video and track objects
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)

        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 225))

        # show frame
        cv2.imshow('MultiTracker', frame)

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break
