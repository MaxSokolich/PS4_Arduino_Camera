from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from PS4.ArduinoHandler import ArduinoHandler
import numpy as np
import time
import multiprocessing
import EasyPySpin
import cv2
from Tracking.FPSCounter import FPSCounter
"""
Axis 0 = LX
Axis 1 = LY
Axis 2 = LT
Axis 3 = RX
Axis 4 = RY
Axis 5 = RT
"""

class MyController:
    def __init__(self):
        self.right_stick = [0,0]
        self.left_stick = [0,0]


        #initlize actions actions
        self.Bx, self.By, self.Bz = 0,0,0
        self.Mx, self.My, self.Mz = 0,0,0
        self.alpha, self.gamma, self.freq = 0,0,0
        self.acoustic_status = 0
        self.stop = 0

        #initilze queue
        self.queue = None
        self.conn = None
        self.arduino = None

    def print_add(self, joy):
        print('CONNECTING JOYSTICK', joy)

    def print_remove(self, joy):
        print('Removed', joy)

    
    def run(self, arduino):
        #self.queue = joystick_q
        #self.conn = conn
        self.arduino = arduino
        run_event_loop(self.print_add, self.print_remove, self.key_received)

    def key_received(self, key):
        #print('Key:', key)
        
        #DISCONNECT
        if key == "Button 1":
            print("DISCONNECTING JOYSTICK")
            self.stop = 1
            

        #LEFT JOYSTICK ORIENT
        if key == "Axis 0" or key == "-Axis 0":
            self.left_stick[0] = round(key.value,3)
            self.Bx = round(key.value,3)

        if key == "Axis 1" or key == "-Axis 1":
            self.left_stick[1] = -round(key.value,3)
            self.By = -round(key.value,3)


        #ACOUSTIC MODULE
        if key == "Button 0":
            self.acoustic_status = key.value
            

        #MAGNETIC FIELD SPIN
        if key == "Button 2":
            if key.value == 1:
                self.gamma = 0
                self.freq = 10
            else:
                self.gamma = 0
                self.freq = 0


        #MAGNETIC FIELD POSITIVE Z
        if key == "Button 5":
            self.Bz = key.value


        #MAGNETIC FIELD NEGATIVE Z
        if key == "Button 4":
            self.Bz = -key.value


        #RIGHT JOYSTICK ROLL
        if key == "Axis 3" or key == "-Axis 3":
            self.right_stick[0] = round(key.value,3)
            x = self.right_stick[0]
            y = self.right_stick[1]
            if self.right_stick == [0,0]:
                self.alpha = 0
                self.gamma = 0
                self.freq = 0

            elif x == 0 and y > 0:
                self.alpha = 0
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)
                
            elif x == 0 and y < 0:
                self.alpha = -np.pi
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)
            else:
                angle = np.arctan2(y,x) - np.pi/2 
                self.alpha = round(angle,3)
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)


        if key == "Axis 4" or key == "-Axis 4":
            self.right_stick[1] = -round(key.value,3)
            x = self.right_stick[0]
            y = self.right_stick[1]
            if self.right_stick == [0,0]:
                self.alpha = 0
                self.gamma = 0
                self.freq = 0

            elif x == 0 and y > 0:
                self.alpha = 0
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)
                
            elif x == 0 and y < 0:
                self.alpha = -np.pi
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)
            else:
                angle = np.arctan2(y,x) - np.pi/2 
                self.alpha = round(angle,3)
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((x)**2 + (y)**2)*20)

        
        if key != "Hat 0 [Centered]":

            #STAGE MOTOR POSITIVE X
            if key == "Hat 0 [Right]":
                self.Mx = key.value-1
            
            #STAGE MOTOR NEGATIVE X
            if key == "Hat 0 [Left]":
                self.Mx = -(key.value-7) 
            
            #STAGE MOTOR POSITIVE Y
            if key == "Hat 0 [Up]":
                self.My = key.value
            
            #STAGE MOTOR NEGATIVE Y
            if key == "Hat 0 [Down]":
                self.My = -(key.value-3)
        if key == "Hat 0 [Centered]":
            self.Mx, self.My = 0,0
        
            
          
        
        
        #STAGE MOTOR POSITIVE Z
        if key == "Axis 5":
            self.Mz = round(key.value,3)
        
        #STAGE MOTOR NEGATIVE Z
        if key == "Axis 2":
            self.Mz = -round(key.value,3)




        #PUT IT ALL TOGETHER
        actions = [self.Bx, 
                   self.By,
                   self.Bz,
                   self.Mx, 
                   self.My, 
                   self.Mz,
                   self.alpha, 
                   round(self.gamma,3), 
                   self.freq,
                   self.acoustic_status,
                   self.stop]
        
        #time.sleep(50/1000)
        #self.queue.put(actions)
       
        #self.conn.send(actions)
        Bx,By,Bz,Mx,My,Mz,alpha,gamma,freq,acoustic_status,stop = actions
        arduino.send(Bx,By,Bz,alpha,gamma,freq)

        #EXIT CONDITION
        if self.stop == 1:
            Joystick.close()
            arduino.send(0,0,0,0,0,0)
            arduino.close()
            #self.stop()

        
class MyCamera:
    def __init__(self):
        pass
    def run(self, arduino):
        #create fps instance
        fps_counter = FPSCounter()

        #connect to camera
        cam = EasyPySpin.VideoCapture(0)
        w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))


        while True:
            fps_counter.update()
            success, frame = cam.read()
            cv2.putText(frame,str(int(fps_counter.get_fps())),(int(w / 40),int(h / 30)),cv2.FONT_HERSHEY_COMPLEX,0.5,(255, 255, 255),1,)
            cv2.imshow("im", frame)
           
        
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        cam.release()
        cv2.destroyAllWindows()           
   


if __name__ == "__main__":
    #connect to arduino
    PORT = "/dev/ttyACM0"
    arduino = ArduinoHandler()
    arduino.connect(PORT)

    #connect and run joystick process
    Controller = MyController()
    joystick_process = multiprocessing.Process(target = Controller.run, args = (arduino,))
    

    #connect and run camera process
    Camera = MyCamera()
    camera_process = multiprocessing.Process(target = Camera.run, args = (arduino,))
    

    #start both processes simutaneously
    camera_process.start()
    joystick_process.start()
    camera_process.join()
    joystick_process.join()
    




    
            


