## Casey Astiz & Nick Cogswell 701
## code to be run on Raspberry pi
## captures video and returns as arrays

import numpy as np
import cv2

#def capture_video():
#    """
 #   Capture video from the webcam and transform it into matrices
  #  """
 #   cap = cv2.VideoCapture(0)

#    while(True):
    # Capture frame-by-frame
  #      ret, frame = cap.read()

        # Our operations on the frame come here
   ##     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
     #   cv2.imshow('frame',gray)
      #  if cv2.waitKey(1) & 0xFF == ord('q'):
       #     break

        # When everything done, release the capture
       ### cap.release()
        #cv2.destroyAllWindows()

cam = cv2.VideoCapture(0)
s, im = cam.read() # captures image
#cv2.imshow("Test Picture", im) # displays captured image
cv2.imwrite("test.bmp",im) # writes image test.bmp to disk

#might be able to do just this
#x_data = np.array( [np.array(cv2.imread(imagePath[i])) for i in range(len(imagePath))] )

#pixels = x_data.flatten().reshape(1000, 12288)
#print (pixels.shape)
