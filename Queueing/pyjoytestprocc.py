from queue import Empty
from pyjoytest import MyController
from PS4.ArduinoHandler import ArduinoHandler
from PS4.MotorStageClass import MotorStage

import multiprocessing 
#from src.python.AcousticClass import AcousticClass
import time

"""
Bx             : magnetic field in x
By             : magnetic field in y
Bz             : magnetic field in z
Mx             : stage motor in x
My             : stage motor in y
Mz             : stage motor in z
alpha          : rolling polar angle 
gamma          : rolling azimuthal angle
freq.          : rolling frequency
acoustic_status: acoustic module status on or off
"""





if __name__ == "__main__":
    #create instance of motor stage class
    stage = MotorStage()

    #create instance and connect to arduino module
    PORT = "/dev/ttyACM0"
    arduino = ArduinoHandler()
    arduino.connect(PORT)
    
    #create queue  to handle joystick commands
    joystick_queue = multiprocessing.Queue()
    controller = MyController()
    
    joystick_process = multiprocessing.Process(target = controller.run, args = (joystick_queue,))
    joystick_process.start()



 
    while True:
      
        try:
            actions = joystick_queue.get(-1)
            Bx,By,Bz,Mx,My,Mz,alpha,gamma,freq,acoustic_status,stop = actions
            

            if stop == 1:
                print("breaking")
                break
            
            print("queue contents = ", actions)
            #send Mx,My,Mz via adarduit motorkit libaray, not arduino for now
            


        except Empty:
            pass

        #time.sleep(23/1000)
        #finally:
         
        
 
    joystick_process.close()
    joystick_process.join()
    stage.stop()
    arduino.close()


