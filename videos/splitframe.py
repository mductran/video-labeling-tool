import cv2
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', type=str, help='video input', required=True)
ap.add_argument('-f', type=int, help='amount of frame to skip', required=True)
args = vars(ap.parse_args())

filename = args.get('video')[:-4]

vidcap = cv2.VideoCapture(args.get('video'))
success,image = vidcap.read()
count = 0

# number of frames to skip
numFrameToSave = args.get('f')

print ("success")
while success: # check success here might break your program
  success,image = vidcap.read() #success might be false and image might be None
  #check success here
  if not success:
    break
  
  # on every numFrameToSave
  if (count % numFrameToSave ==0):
    if os.path.isdir('images'):
      path = os.path.join('images', '{}_%d.jpg'.format(filename)%count)
      cv2.imwrite(path, image)
    else:
      os.mkdir('images')
      path = os.path.join('images', '{}_%d.jpg'.format(filename)%count)
      cv2.imwrite(path, image)
          
  if cv2.waitKey(10) == 27:
      break
  count += 1

print('done')
