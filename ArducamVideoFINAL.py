import numpy as np
import cv2
from camera import Camera

class ArduCam(Camera):
    
    def __init__(self, location):
        self.location = location

  
    def register(self):
        self.cap = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None

    
    def record(self):
        self.out = cv2.VideoWriter('Video.avi {self.location}', self.fourcc, 20.0, (640, 480))
        ret, frame = self.cap.read()
        if ret == True:
            # write the frame to file
            self.out.write(frame)

            # display the resulting frame
            cv2.imshow('frame',frame)
    
    def stop(self):
        # Release everything if job is finished
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()


# while True:
#             ret, frame = self.cap.read()
#             if ret == True:
#                 # write the frame to file
#                 self.out.write(frame)

#                 # display the resulting frame
#                 cv2.imshow('frame',frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break
#             else:
#                 break