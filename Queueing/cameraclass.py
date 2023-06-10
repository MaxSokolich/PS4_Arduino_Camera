from queue import Empty
from pyjoytest import MyController
from PS4.ArduinoHandler import ArduinoHandler
from PS4.MotorStageClass import MotorStage

import multiprocessing 
#from src.python.AcousticClass import AcousticClass
import time



def camera_recv(conn):
        while True:
            event = conn.recv()
            #time.sleep(25/1000)
            if event[-1] == 1:
                 break
            print("conn = ", event)
        print("succesful exited process")

def run():
    conn1, conn2 = multiprocessing.Pipe()

    #joystick_queue = multiprocessing.Queue()
    controller = MyController()

    joystick_process = multiprocessing.Process(target = controller.run, args = (conn1,))
    camera_process = multiprocessing.Process(target = camera_recv, args = (conn2,))

    joystick_process.start()
    camera_process.start()
    
    joystick_process.join()
    camera_process.join()
     

if __name__ == "__main__":
     run()
   


    


