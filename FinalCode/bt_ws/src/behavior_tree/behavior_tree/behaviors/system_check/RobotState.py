#!/usr/bin/env python
import logging
import py_trees
from typing import Optional
from py_trees.common import Status
from spot_msgs.action import RobotCommand 
from bdai_ros2_wrappers.action_client import ActionClientWrapper
from bdai_ros2_wrappers.utilities import namespace_with
from spot_msgs.msg import BatteryStateArray
from bosdyn_msgs.conversions import convert
from rclpy.node import Node
from behavior_tree.behaviors.robot_control_behaviors.SpotBehaviors import Behaviours


class RobotState(py_trees.behaviour.Behaviour):
    def __init__(self, name: str,robot_name: Optional[str], node: Optional[Node], logger: logging.Logger):
        super().__init__(name=name)
        self.robot_name = robot_name
        self.node = node  
        self.robot = None
        self.logger = logger

        self.wifi_status = None
        self.charge_percentage = None

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
            self.battery_sub = self.node.create_subscription(BatteryStateArray, '/status/battery_states', self.status_charge_percentage_callback, 10)
        except Exception as e: 
            self.logger.error(str(e))

        
    def initialise(self) -> None:
        pass

    def update(self) -> Status:
        try: 
            if self.charge_percentage is not None:
                if self.charge_percentage < 30.0:
                    self.action_goal, self.proto_goal, self.action_name =self.Behaviours.power_off()
                    if self.action_goal is not None: 
                        convert(self.proto_goal[0], self.action_goal[0].command)
                        self.robot_command_client.send_goal_and_wait(self.action_name, self.action_goal[0], 0.5)
                    py_trees.blackboard.Blackboard.set("system_check", "low battery. Powering off")
                    py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                    py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
                    
                    self.logger.error("battery below 30%")

                return py_trees.common.Status.SUCCESS
            else:
                return py_trees.common.Status.RUNNING

        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE 
    
    def status_wifi_callback(self, msg) -> None:
        if msg:
            self.wifi_status = msg.current_mode

    def status_charge_percentage_callback(self, msg:BatteryStateArray) -> None:
        try:
            if msg:
                self.charge_percentage = msg.battery_states[0].charge_percentage
        except Exception as e:
            self.logger.error("Can't get charge percentage")

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

