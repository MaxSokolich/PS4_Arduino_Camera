
import multiprocessing
from PS4 import MyController
from Camera import MyCamera
from Arduino import MyArduino

"""
press Q on keyboard to close camera window
press Circle on controller to close controller
"""

if __name__ == "__main__":
    #connect to arduino
    PORT = "/dev/ttyACM0"
    arduino = MyArduino()
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
    




    
            


