from pyjoystick.sdl2 import Key, Joystick, run_event_loop, quit, stop_event_wait
import numpy as np
import time
"""
if linux:
    RX = Axis 3
    RY = Axis 4

if Mac:
    RX = Axis 2
    RY = Axis 3
    LT = Axis 4
    RT = Axis 5
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

    
        self.message = []

        #initilze queue
        self.queue = None
        self.conn = None
        self.arduino = None


        
        

        
    def print_add(self, joy):
        print('CONNECTING JOYSTICK', joy)

    def print_remove(self, joy):
        print('Removed', joy)

    def run(self, arduino, queue):
        self.queue = queue
        #self.conn = conn
        self.arduino = arduino
        run_event_loop(self.print_add, self.print_remove, self.key_received)
    
        

    def key_received(self, key):
        #print('Key:', key)
        

        
        #DISCONNECT
        if key == "Button 1":
            print("DISCONNECTING JOYSTICK")
            self.stop = 1
    

        #ACOUSTIC MODULE
        if key == "Button 0":
            self.acoustic_status = key.value
            

        #MAGNETIC FIELD SPIN
        if key == "Button 3":
            if key.value == 1:
                self.gamma = 0
                self.freq = 10
            else:
                self.gamma = 0
                self.freq = 0


        #MAGNETIC FIELD POSITIVE Z
        if key == "Button 10":
            self.Bz = key.value


        #MAGNETIC FIELD NEGATIVE Z
        if key == "Button 9":
            self.Bz = -key.value        
       

        #STAGE MOTOR POSITIVE X
        if key == "Button 14":
            self.Mx = key.value
        
        #STAGE MOTOR NEGATIVE X
        if key == "Button 13":
            self.Mx = -(key.value) 
        
        #STAGE MOTOR POSITIVE Y
        if key == "Button 11":
            self.My = key.value
        
        #STAGE MOTOR NEGATIVE Y
        if key == "Button 12":
            self.My = -(key.value)
      






        
        #LEFT JOYSTICK ORIENT
        if key == "Axis 1" or key == "-Axis 1":
            #self.left_stick[0] = round(key.value,3)
            self.Bx = round(key.value,3)

        if key == "Axis 0" or key == "-Axis 0":
            #self.left_stick[1] = -round(key.value,3)
            self.By = -round(key.value,3)


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


        if key == "Axis 2" or key == "-Axis 2":
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


        
        #STAGE MOTOR POSITIVE Z
        if key == "Axis 5":
            self.Mz = round(key.value,3)
        
        #STAGE MOTOR NEGATIVE Z
        if key == "Axis 4":
            self.Mz = -round(key.value,3)


        #PUT IT ALL TOGETHER
        
        
        self.actions = [self.Bx, 
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
        
        #self.message.append(self.actions)
        
        self.queue.put(self.actions)
        

        
        #we dont want to put actions in the queue always 
        

        #self.counter +=1
        #if (self.counter % 10) == 0:
        
        #time.sleep(50/1000)
        #print(self.actions)

       
        

        Bx,By,Bz,Mx,My,Mz,alpha,gamma,freq,acoustic_status,stop = self.actions
        
      
        #self.arduino.send(Bx,By,Bz,alpha,gamma,freq)

        #EXIT CONDITION
        if self.stop == 1:
            Joystick.close()
            #quit()
            #stop_event_wait()
            #self.arduino.send(0,0,0,0,0,0)
            #self.arduino.close()
            #self.stop()

"""Controller = MyController()
Controller.run(None,None)"""