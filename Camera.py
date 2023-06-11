#import EasyPySpin
import cv2
from src.FPSCounter import FPSCounter
from queue import Empty


class MyCamera:
    def __init__(self):
         #create fps instance
        self.fps_counter = FPSCounter()
    def run(self, arduino, queue):
        
        
        #connect to camera
        cam = cv2.VideoCapture("/Users/bizzarohd/Desktop/spinningmanipulation2.mov")
        w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))


        while True:
            try:
                event = queue.get(0)
                print("contents = ", event)
            except Empty:
                pass
            

            #success, frame = cam.read()
            #cv2.putText(frame,str(int(self.fps_counter.get_fps())),(int(w / 40),int(h / 30)),cv2.FONT_HERSHEY_COMPLEX,0.5,(255, 255, 255),1,)
            #cv2.imshow("im", frame)
           
        
            #if cv2.waitKey(1) & 0xFF == ord("q"):
            #    break
        
        cam.release()
        cv2.destroyAllWindows()           