#!/usr/bin/env python
import logging
import py_trees
import threading
from threading import Event
from rclpy.node import Node
from typing import Optional
from py_trees.common import Status
from .SpotBehaviors import Behaviours
from spot_msgs.action import RobotCommand 
from bosdyn_msgs.conversions import convert
from bdai_ros2_wrappers.utilities import namespace_with
from bdai_ros2_wrappers.action_client import ActionClientWrapper

# Global Variables
stop_moving = False

class RobotControl(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, robot_name: Optional[str], node: Optional[Node], task: str, logger: logging.Logger):
        super().__init__(name=name)
        self.task = task
        self.robot_name = robot_name
        self.node = node  
        self.logger = logger

    def setup(self, **kwargs) -> None:
        try:
            self.event = Event()
            self.node = kwargs['node']
            self.Behaviours = Behaviours(self.node, self.robot_name, logger=self.logger)
        except Exception as e: 
            self.logger.error(str(e))
            
        
    def initialise(self) -> None:
        global stop_moving
        stop_moving = False
        self.execution_started = False
        self.action_goals = [] 
        self.proto_goals = []
        self.action_name = ""
        self.execution_thread = None
        self.event.clear()

    def update(self) -> Status:
        global stop_moving
        try: 
            if self.execution_started is False: 
                if self.task and hasattr(self.Behaviours, self.task):
                    command_function = getattr(self.Behaviours, self.task)
                    self.action_goals, self.proto_goals, self.action_name = command_function() 
                    self.execution_thread = threading.Thread(target=command_execution, args=(self.event, self.robot_name, self.node, self.action_goals, self.proto_goals, self.action_name, self.logger,))
                    self.execution_thread.start()
                    self.execution_started = True
            else: 
                if not self.execution_thread.is_alive():
                    return py_trees.common.Status.SUCCESS
            return py_trees.common.Status.RUNNING

        except Exception as e: 
            self.logger.error(str(e))
            return py_trees.common.Status.FAILURE 
    
    def terminate(self, new_status: Status) -> None:
        self.event.set()
        return super().terminate(new_status)

def command_execution(event: Event, robot_name: str, node: Node, action_goals: list, proto_goals: list, action_name: str, logger: logging.Logger):
    try:
        global stop_moving
        
        robot_command_client = ActionClientWrapper(
                RobotCommand, namespace_with(robot_name, "robot_command"), node)
        if action_goals is not None: 
            for i in range(len(action_goals)):
                if not event.is_set():
                    if stop_moving is False:
                            convert(proto_goals[i], action_goals[i].command)
                            robot_command_client.send_goal_and_wait(action_name, action_goals[i])

                    else: # For example if object is found
                        action_goals, proto_goals, action_name = Behaviours.stand()
                        if action_goals is not None:
                            convert(proto_goals[0], action_goals[0].command)
                            robot_command_client.send_goal_and_wait(action_name, action_goals[0])
                        break
                else: 
                    break

    except Exception as e: 
        logger.error(str(e))