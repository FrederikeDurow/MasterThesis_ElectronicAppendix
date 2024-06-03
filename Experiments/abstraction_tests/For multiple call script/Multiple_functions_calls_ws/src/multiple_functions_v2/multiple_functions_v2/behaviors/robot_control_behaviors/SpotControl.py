#!/usr/bin/env python
import logging
import py_trees
import rclpy
from typing import Optional
from py_trees.common import Status
#from .SpotBehaviors import Behaviours
#from spot_driver.manual_conversions import c
from bosdyn_msgs.conversions import convert
#from spot_msgs.action import RobotCommand 
#from bdai_ros2_wrappers.action_client import ActionClientWrapper
#from bdai_ros2_wrappers.utilities import namespace_with
# from utilities.simple_spot_commander import SimpleSpotCommander
from rclpy.node import Node
#from spot_msgs.srv import SetVelocity


class RobotControl(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, robot_name: Optional[str], node: Optional[Node], task: str, logger: logging.Logger):
        super().__init__(name=name)
        self.task = task
        self.robot_name = robot_name
        self.node = node  
        self.logger = logger

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']

            # self.cli = self.node.create_client(SetVelocity, "max_velocity")
            # while not self.cli.wait_for_service(timeout_sec=1.0):
            #     self.logger.info("Max_velocity service not available, waiting again...")
            # self.req = SetVelocity.Request()
        except Exception as e: 
            self.logger.error(str(e))
            
        
    def initialise(self) -> None:
        try: 
            # Initialize variables
            self.action_goals = [] 
            self.proto_goals = []
            self.action_name = ""

        except Exception as e:
            self.logger.error(str(e))

    def update(self) -> Status:
        try: 
            return py_trees.common.Status.SUCCESS
        
        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE 
    


    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
