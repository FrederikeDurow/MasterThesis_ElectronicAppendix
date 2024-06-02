#!/usr/bin/env python
import logging
import py_trees
from typing import Optional
from py_trees.common import Status
from .SpotBehaviors import Behaviours
from bosdyn_msgs.conversions import convert
from spot_msgs.action import RobotCommand 
from bdai_ros2_wrappers.action_client import ActionClientWrapper
from bdai_ros2_wrappers.utilities import namespace_with
from rclpy.node import Node

class RobotControl(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, robot_name: Optional[str], node: Optional[Node], task: str, logger: logging.Logger):
        super().__init__(name=name)
        self.task = task
        self.robot_name = robot_name
        self.node = node  
        self.robot = None
        self.logger = logger

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        try: 
            self.robot_command_client = ActionClientWrapper(
                RobotCommand, namespace_with(self.robot_name, "robot_command"), self.node)
            self.Behaviours = Behaviours(self.node, self.robot_name, logger=self.logger)
        except Exception as e: 
            self.logger.error(str(e))
        
    def initialise(self) -> None:
        self.action_goal = None
        self.proto_goal = None
        self.action_name = ""

    def update(self) -> Status:
        try: 
            if self.task and hasattr(self.Behaviours, self.task):
                command_function = getattr(self.Behaviours, self.task)
                self.action_goal, self.proto_goal, self.action_name = command_function()
                
            if self.action_goal is not None: 
                pass
                convert(self.proto_goal, self.action_goal.command)
                self.robot_command_client.send_goal_and_wait(self.action_name, self.action_goal, 0.5)
            return py_trees.common.Status.SUCCESS
        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE 

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

