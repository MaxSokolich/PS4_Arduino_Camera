
#import os
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import multiprocessing
import threading

from PS4_Mac import MyController
from Camera import MyCamera
from Arduino import MyArduino

"""
remember to change the PS4_() to correct operating system
press Q on keyboard to close camera window
press Circle on controller to close controller
"""
PORT = "/dev/cu.usbmodem11401" # "COM3"# "/dev/ttyACM0" # "/dev/cu.usbmodem11301"
output_video_name = "/Users/bizzarohd/Desktop/testvife"


if __name__ == "__main__":
    #connect to arduino
    arduino = MyArduino()
    arduino.connect(PORT)

    #create a queue to communicate information between joystick process and camera process
    queue = multiprocessing.Queue(1)  #need the 1 here


    #connect and run controller in seperate process
    Controller = MyController()
    joystick_process = multiprocessing.Process(target = Controller.run, args = (queue,))
    joystick_process.start()

    #run camera
    Camera = MyCamera(output_video_name)
    Camera.run(queue,arduino)

    

    
    




    
            


