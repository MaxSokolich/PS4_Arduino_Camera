#import EasyPySpin
import cv2
#from FPSCounter import FPSCounter
from Tracker import Tracker
from Params import CONTROL_PARAMS, CAMERA_PARAMS


class MyCamera:
    """
    to handle all aspects of tracking, detecting microrobots using FLIR camera
    """
    def __init__(self):
        #connect to cam
        self.cam = cv2.VideoCapture("/Users/bizzarohd/Desktop/spinningmanipulation2.mov")#cv2.VideoCapture(0)  #EasyPySpin.VideoCapture(0)
        self.w = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        #create mytracker instance
        self.Tracker = Tracker(self.w,self.h)



    def run(self, queue, arduino):
        """
        run camera with tracking software if appliciable
        """
        
        #create a window and name it "im"
        cv2.namedWindow("Max's Tracker")

        while True:

            #read_data_from joystick


            #read frame
            success, frame = self.cam.read()

            #run tracker
            frame, robot_list = self.Tracker.run("Max's Tracker", frame)
    
            #analyze robot_list
            #CONTROL ALGORITHM GOES HERE

            
            #output to arduino
            
            

            #show frame
            cv2.imshow("Max's Tracker", frame)
           
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
          
        self.cam.release()
        cv2.destroyAllWindows() 


c = MyCamera()
c.run(None,None)