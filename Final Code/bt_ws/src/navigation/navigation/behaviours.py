import argparse
import logging
import math

from typing import Optional

import bdai_ros2_wrappers.process as ros_process
import bdai_ros2_wrappers.scope as ros_scope
from bdai_ros2_wrappers.action_client import ActionClientWrapper
from bdai_ros2_wrappers.utilities import fqn, namespace_with
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, VISION_FRAME_NAME
from bosdyn.client.math_helpers import SE2Pose
from bosdyn.client.robot_command import RobotCommandBuilder
from rclpy.node import Node
from utilities.simple_spot_commander import SimpleSpotCommander
from utilities.tf_listener_wrapper import TFListenerWrapper

import spot_driver.conversions as conv
from spot_msgs.action import RobotCommand  # type: ignore

# Where we want the robot to walk to relative to itself
ROBOT_T_GOAL = SE2Pose(1.0, 0.0, 0.0)



class Behaviours:
    def __init__(self, node: ros_scope.node(), robot_name) -> None:
        self._logger = logging.getLogger(fqn(self.__class__))
        self._robot_name = robot_name
        self._tf_listener = TFListenerWrapper(node)
        self._tf_listener.wait_for_a_tform_b(self._body_frame_name, self._vision_frame_name)

        self._body_frame_name = namespace_with(self._robot_name, BODY_FRAME_NAME)
        self._vision_frame_name = namespace_with(self._robot_name, VISION_FRAME_NAME)


    def walk_forward_with_world_frame_goal(self) -> None:
        self._logger.info("Walking forward")
        world_t_robot = self._tf_listener.lookup_a_tform_b(
            self._vision_frame_name, self._body_frame_name
        ).get_closest_se2_transform()
        world_t_goal = world_t_robot * ROBOT_T_GOAL
        proto_goal = RobotCommandBuilder.synchro_se2_trajectory_point_command(
            goal_x=world_t_goal.x,
            goal_y=world_t_goal.y,
            goal_heading=world_t_goal.angle,
            frame_name=VISION_FRAME_NAME,  # use Boston Dynamics' frame conventions
        )
        action_goal = RobotCommand.Goal()
        return action_goal, proto_goal, "walk_forward"
        
    
    def turn20(self) -> None:
        self._logger.info("Turning 20 degrees")
        world_t_robot = self._tf_listener.lookup_a_tform_b(
            self._vision_frame_name, self._body_frame_name
        ).get_closest_se2_transform()
        world_t_goal = world_t_robot * SE2Pose(0.0, 0.0, math.radians(20))
        proto_goal = RobotCommandBuilder.synchro_se2_trajectory_point_command(
            goal_x=world_t_goal.x,
            goal_y=world_t_goal.y,
            goal_heading=world_t_goal.angle,
            frame_name=VISION_FRAME_NAME,  # use Boston Dynamics' frame conventions
        )
        action_goal = RobotCommand.Goal()
        return action_goal, proto_goal, "turn"
        



