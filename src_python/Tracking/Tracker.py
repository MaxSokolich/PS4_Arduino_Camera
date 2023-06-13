
import cv2
import time
import matplotlib.pyplot as plt
from FPSCounter import FPSCounter
from Params import CONTROL_PARAMS, CAMERA_PARAMS
from typing import List, Tuple, Union
import numpy as np
from typing import List, Tuple, Union
import numpy as np


from math import sqrt

def get_magnitude(x:float, y:float, z:float) -> float:
    """
    Return the magnitude of this velocity vector

    Args:
        None
    Returns:
        Velocity's magnitude as a float
    """
    return sqrt(x**2 + y**2 + z**2)

class Velocity:
    """
    Contains information on a Robot's x and y velocity, alongside
    its "z" velocity, represented by its blurring measure.

    Args:
        x: velocity along the x coordinate
        y: velocity along the y coordinate
        z: velocity along the z coordinate
    """

    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z
        self.mag = get_magnitude(x, y, z)



class Robot:
    """
    Robot class to store and ID all new robots currently being tracked.

    Args:
        None
    """

    def __init__(self):
        self.velocity_list = []  # stores bot velocities per frame
        self.position_list = []  # stores bot positions per frame
        self.cropped_frame = []  # cropped section of a frame representing the bot
        self.trajectory = []  # track points from manual pathing
        self.area_list = []  # stores the cropped areas
        self.avg_area = 0  # current average area of the bot in this frame

    def add_velocity(self, velocity: Velocity):
        self.velocity_list.append(velocity)

    def add_position(self, position: List[float]):
        self.position_list.append(position)
 
    def add_crop(self, crop: List[int]):
        self.cropped_frame.append(crop)

    def add_trajectory(self, traj: List[int]):
        self.trajectory.append(traj)

    def add_area(self, area: float):
        self.area_list.append(area)

    def set_avg_area(self, avg_area: float):
        self.avg_area = avg_area





class Tracker:

    def __init__(self,width,height):
        self.start = time.time()
        self.draw_trajectory = False  # determines if trajectory is manually being drawn
        self.robot_list = []  # list of actively tracked robots
        
        
        self.control_params = CONTROL_PARAMS
        self.camera_params = CAMERA_PARAMS

        self.width = width  # width of cv2 window
        self.height = height  # height of cv2 window

        self.num_bots = 0  # current number of bots

        self.fps_counter = FPSCounter()
        self.pix_2metric = 1#((resize_ratio[1]/106.2)  / 100) * self.camera_params["Obj"] 


    def mouse_points(self, event: int, x: int, y: int, flags, params):

              # Left button mouse click event; creates a RobotClass instance
            if event == cv2.EVENT_LBUTTONDOWN:
                # click on bot and create an instance of a mcirorobt
                # CoilOn = False
                bot_loc = [x, y]

                #create upper and lower bounds from point click color
        
                #generate original bounding box
                x_1 = int(x - self.control_params["initial_crop"] / 2)
                y_1 = int(y - self.control_params["initial_crop"] / 2)
                w = self.control_params["initial_crop"]
                h = self.control_params["initial_crop"]



                robot = Robot()  # create robot instance
                robot.add_position(bot_loc)  # add position of the robot
                robot.add_crop([x_1, y_1, w, h])
                self.robot_list.append(robot)

                # add starting point of trajectory
                self.robot_list[-1].add_trajectory(bot_loc)
                self.num_bots += 1


            # Right mouse click event; allows you to draw the trajectory of the
            # most currently added microbot, so long as the button is held
            elif event == cv2.EVENT_RBUTTONDOWN:
                # draw trajectory
                target = [x, y]
                # create trajectory
                self.robot_list[-1].add_trajectory(target)
                self.draw_trajectory = True  # Target Position

            # Works in conjunction with holding down the right button for drawing
            # the trajectory
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.draw_trajectory:
                    target = [x, y]
                    self.robot_list[-1].add_trajectory(target)

            # When right click is released, stop drawing trajectory
            elif event == cv2.EVENT_RBUTTONUP:
                self.draw_trajectory = False

            # Middle mouse; CLEAR EVERYTHING AND RESTART ANALYSIS
            elif event == cv2.EVENT_MBUTTONDOWN:
                #reset algorothms i.e. set node back to 0

                self.num_bots = 0
                del self.robot_list[:]

        
    def track_robot(self, frame, fps_counter):
        """
        For each robot defined through clicking, crop a frame around it based on initial
        left mouse click position, then:
            - apply mask and find contours
            - from contours draw a bounding box around the contours
            - find the centroid of the bounding box and use this as the robots current position

        Args:
            frame: np array representation of the current video frame read in
        Returns:
            None
        """
        for bot in range(len(self.robot_list)):
            
            
            # crop the frame based on initial ROI dimensions
            x_1, y_1, x_2, y_2 = self.robot_list[bot].cropped_frame[-1]
            
            max_width = 0  # max width of the contours
            max_height = 0  # max height of the contours

            x_1 = max(min(x_1, self.width), 0)
            y_1 = max(min(y_1, self.height), 0)
         
        
            cropped_frame = frame[y_1 : y_1 + y_2, x_1 : x_1 + x_2]

            crop_mask = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            lower_thresh =  self.control_params["lower_thresh"]
            upper_thresh = self.control_params["upper_thresh"]
            crop_mask = cv2.inRange(crop_mask, lower_thresh, upper_thresh)
            
            contours, _ = cv2.findContours(crop_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
    
            if len(contours) !=0:
               
                max_cnt = contours[0]
                for contour in contours:
                    # alcualte max_contour
                   
                    if cv2.contourArea(contour) > cv2.contourArea(max_cnt): 
                        max_cnt = contour

                area = cv2.contourArea(max_cnt)* (1/self.pix_2metric**2)
                
                x, y, w, h = cv2.boundingRect(max_cnt)
                current_pos = [(x + x + w) / 2, (y + y + h) / 2]
                # track the maximum width and height of the contours
                if w > max_width:
                    max_width = w*self.control_params["tracking_frame"]
                if h > max_height:
                    max_height = h*self.control_params["tracking_frame"]
                
                cv2.drawContours(cropped_frame, [max_cnt], -1, (0, 255, 255), 1)

                
                #begin tracking part
                self.robot_list[bot].add_area(area)
                avg_global_area = sum(self.robot_list[bot].area_list) / len(self.robot_list[bot].area_list)
                self.robot_list[bot].set_avg_area(avg_global_area)

                #create new cropped frame
                x_1_new = x_1 + current_pos[0] - max_width
                y_1_new = y_1 + current_pos[1] - max_height
                x_2_new = 2* max_width
                y_2_new = 2* max_height
                new_crop = [int(x_1_new), int(y_1_new), int(x_2_new), int(y_2_new)]
                

                if len(self.robot_list[bot].position_list) > 0:
                    velx = (
                        (current_pos[0] + x_1 - self.robot_list[bot].position_list[-1][0])) 

                    vely = (
                        (current_pos[1] + y_1 - self.robot_list[bot].position_list[-1][1]))
        
                    vel = Velocity(velx, vely, 0)
                    self.robot_list[bot].add_velocity(vel)
                
                # update robots params
                self.robot_list[bot].add_crop(new_crop)
                self.robot_list[bot].add_position([current_pos[0] + x_1, current_pos[1] + y_1])


        

    def display_hud(self, frame: np.ndarray,fps: FPSCounter):
        """
        Display dragon tails (bot trajectories) and other HUD graphics

        Args:
            frame: np array representation of the current video frame read in
        Returns:
            None
        """
        w = frame.shape[0]
        h = frame.shape[1]
        
        #fps
        fps.update()
        cv2.putText(frame,str(int(fps.get_fps())),
            (int(w / 40),int(h / 30)),
            cv2.FONT_HERSHEY_COMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        if len(self.robot_list) > 0:
            color = plt.cm.rainbow(np.linspace(0, 1, self.num_bots)) * 255
            # bot_ids = [i for i in range(self.num_bots)]
            for (
                bot_id,
                bot_color,
            ) in zip(range(self.num_bots), color):

                x = int(self.robot_list[bot_id].cropped_frame[-1][0])
                y = int(self.robot_list[bot_id].cropped_frame[-1][1])
                w = int(self.robot_list[bot_id].cropped_frame[-1][2])
                h = int(self.robot_list[bot_id].cropped_frame[-1][3])

                # display dragon tails
                pts = np.array(self.robot_list[bot_id].position_list, np.int32)
                cv2.polylines(frame, [pts], False, bot_color, 2)
                

                #display target positions
                targets = self.robot_list[bot_id].trajectory
                if len(targets) > 0:
                    pts = np.array(self.robot_list[bot_id].trajectory, np.int32)
                    cv2.polylines(frame, [pts], False, (1, 1, 255), 2)


                    tar = targets[-1]
                    cv2.circle(frame,
                        (int(tar[0]), int(tar[1])),
                        4,
                        (bot_color),
                        -1,
                    )

                
                
                dia = round(np.sqrt(4*self.robot_list[bot_id].avg_area/np.pi),1)
                text = "robot {}: {} px ".format(bot_id+1,dia)
                
                cv2.putText(frame, "robot {}".format(bot_id+1), (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
                cv2.putText(frame, "~ {}px".format(dia), (x, y+h+20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                            
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                
                # if there are more than 10 velocities recorded in the robot, get
                # and display the average velocity
                if len(self.robot_list[bot_id].velocity_list) > 10:
                    # a "velocity" list is in the form of [x, y, magnitude];
                    # get the magnitude of the 10 most recent velocities, find their
                    # average, and display it on the tracker
                    vmag = [v.mag for v in self.robot_list[bot_id].velocity_list[-10:]]
                    vmag_avg = round(sum(vmag) / len(vmag),2)
                    
                    cv2.putText(frame, f'{vmag_avg:.1f} px/s', (x, y +h + 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                    
                    text = "robot {}: {} px | {} px/s ".format(bot_id+1,dia,vmag_avg)
                cv2.putText(
                    frame,
                    text,
                    (0, 170 + bot_id * 20),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    bot_color,
                    1,
                )

    def run(self,window, frame):
        
        #initilize mouse click callbacks
        cv2.setMouseCallback(window, self.mouse_points)

        #listen for mouse clicks to detect robots
        self.track_robot(frame, self.fps_counter)

        #display heads up display
        self.display_hud(frame, self.fps_counter)

        #return the updated frame
        return frame, self.robot_list