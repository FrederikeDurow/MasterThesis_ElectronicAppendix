#!/usr/bin/env python
import logging
import py_trees
from typing import Optional
from py_trees.common import Status
#import spot_driver.conversions as conv
from spot_msgs.action import RobotCommand 
from bdai_ros2_wrappers.action_client import ActionClientWrapper
from bdai_ros2_wrappers.utilities import namespace_with
from bosdyn_msgs.conversions import convert
from behavior_tree.behaviors.robot_control_behaviors.SpotBehaviors import Behaviours
from rclpy.node import Node

class Bootup(py_trees.behaviour.Behaviour):
    def __init__(self, name: str,robot_name: Optional[str], node: Optional[Node], logger: logging.Logger):
        super().__init__(name=name)
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
        pass

    def update(self) -> Status:
        try: 
            py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW")
            return py_trees.common.Status.SUCCESS
        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE 

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
