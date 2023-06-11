import asyncio
import time
import cv2
from src.FPSCounter import FPSCounter
from queue import Empty


async def tcp_print_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8898)


    message = ''
    cam = cv2.VideoCapture("/Users/bizzarohd/Desktop/spinningmanipulation2.mov")
    w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_counter = FPSCounter()

    while True:
        data = await reader.read(4096)
        message = data.decode('utf-8')
        print("message", message)


        success, frame = cam.read()
        cv2.putText(frame,str(int(fps_counter.get_fps())),(int(w / 40),int(h / 30)),cv2.FONT_HERSHEY_COMPLEX,0.5,(255, 255, 255),1,)
        cv2.imshow("im", frame)
        
    
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    

    cam.release()
    cv2.destroyAllWindows()  
    print('Close the connectioß')
    writer.close()
    await writer.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_print_client())