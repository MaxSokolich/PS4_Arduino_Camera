import cv2
import pygame
import time
import numpy as np

class pygamejoy:
    def __init__(self):

        #initlize actions actions
        self.Bx, self.By, self.Bz = 0,0,0
        self.Mx, self.My, self.Mz = 0,0,0
        self.alpha, self.gamma, self.freq = 0,0,0
        self.acoustic_status = 0
        self.stop = 0


        self.queue = None
        self.arduino = None

    


    def run(self, arduino, queue):
        self.arduino = arduino
        self.queue = queue

        # Initialize the joystick
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
       
        clock = pygame.time.Clock()
        # Main loop
        while True:

            clock.tick(70) #ms
            lx = joystick.get_axis(0)
            ly = joystick.get_axis(1)
            print(lx)
        

            rx =joystick.get_axis(2)
            ry = joystick.get_axis(3)

            lt = joystick.get_axis(4)
            rt = joystick.get_axis(5)

        
            self.Bx = round(lx,2)
            self.By = round(ly,2)

            self.Mz = -round(lt,3)
            self.Mz = round(rt,3)


            if [rx,ry] == [0,0]:
                self.alpha = 0
                self.gamma = 0
                self.freq = 0

            elif rx == 0 and ry > 0:
                self.alpha = 0
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((rx)**2 + (ry)**2)*20)
                
            elif rx == 0 and ry < 0:
                self.alpha = -np.pi
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((rx)**2 + (ry)**2)*20)
            else:
                angle = np.arctan2(ry,rx) - np.pi/2 
                self.alpha = round(angle,3)
                self.gamma = np.pi/2
                self.freq = int(np.sqrt((rx)**2 + (ry)**2)*20)

                
                self.acoustic_status = joystick.get_button(1)
                
                
            
                if self.acoustic_status == 1:
                    return True
            
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
            print(self.actions)
             
        
         
           


p = pygamejoy()
p.run(None, None)