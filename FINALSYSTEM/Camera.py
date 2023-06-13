#import EasyPySpin
import cv2
from Tracker import Tracker
from Params import CONTROL_PARAMS, CAMERA_PARAMS
from AlgorithmClass import Algorithm
from queue import Empty


class MyCamera:
    """
    to handle all aspects of tracking, detecting microrobots using FLIR camera
    """
    def __init__(self, output_name):
        #connect to cam
        self.cam = cv2.VideoCapture("/Users/bizzarohd/Desktop/spinningmanipulation2.mov")#cv2.VideoCapture(0)  #EasyPySpin.VideoCapture(0)
        self.w = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.cam.set(cv2.CAP_PROP_EXPOSURE, CAMERA_PARAMS["exposure"])
        self.cam.set(cv2.CAP_PROP_FPS, CAMERA_PARAMS["framerate"])

        #create mytracker instance
        self.Tracker = Tracker(self.w,self.h)

        #create algorithm instance
        self.Algorithm = Algorithm()

        #save video object
        if CAMERA_PARAMS["Record"] == True:
            self.result = cv2.VideoWriter(
                            output_name + ".mp4",
                            cv2.VideoWriter_fourcc(*"mp4v"),
                            CAMERA_PARAMS["framerate"],    
                            (self.w,self.h))
        
        #initilize base actions
        self.Bx, self.By, self.Bz = 0,0,0
        self.alpha, self.gamma, self.freq = 0,0,0
                            
                        

    def run(self, queue, arduino):
        
        #create a window and name it "im"
        cv2.namedWindow("Max's Tracker")

        while True:

            #STEP 1: read frame
            success, frame = self.cam.read()

            #STEP 2: run tracker to record robot attibutes
            frame, robot_list = self.Tracker.run("Max's Tracker", frame)
    
            #STEP 3: analyze robot_list and run an algorithm to genreate appropriate magnetic field signals
            self.Bx, self.By, self.Bz, self.alpha, self.gamma, self.freq = self.Algorithm.run(robot_list)

            #STEP 4: read joystick commands to overwrite
            try:
                actions = queue.get(0)   #match this with the tracker commands to save input output data.
                self.Bx,self.By,self.Bz,Mx,My,Mz,self.alpha,self.gamma,self.freq,acoustic_status = actions  
            except Empty: #except if the queue is empty
                pass

            #STEP 4: output to arduino
            if arduino.conn is not None:
                arduino.send(self.Bx, self.By, self.Bz, self.alpha, self.gamma, self.freq)
            
            #STEP 5: record video if true
            if CAMERA_PARAMS["Record"] == True:
                self.result.write(frame)
            
            #STEP 6: show frame
            cv2.imshow("Max's Tracker", frame)
           
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        
        
        if CAMERA_PARAMS["Record"] == True:
            self.result.release()
        if arduino.conn is not None:
            arduino.close()
        
        self.cam.release()
        cv2.destroyAllWindows() 
        


#c = MyCamera(output_name="/Users/bizzarohd/Desktop/testvife")
#c.run(None,None)