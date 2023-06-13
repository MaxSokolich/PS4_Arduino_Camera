#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing the Robot class

@authors: Max Sokolich, Brennan Gallamoza, Luke Halko, Trea Holley,
          Alexis Mainiero, Cameron Thacker, Zoe Valladares
"""

from typing import List, Tuple, Union
import numpy as np





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



    def add_velocity(self, velocity: Velocity):
        self.velocity_list.append(velocity)

    def add_position(self, position: List[float]):
        self.position_list.append(position)
 
    def add_crop(self, crop: List[int]):
        self.cropped_frame.append(crop)

    def add_trajectory(self, traj: List[int]):
        self.trajectory.append(traj)




