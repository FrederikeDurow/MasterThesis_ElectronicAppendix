#!/usr/bin/env python
import argparse
import logging
import math
# from behaviours import Behaviours
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
from std_msgs.msg import String
import time

class Behaviours:
    def __init__(self, robot_name: Optional[str] = None, node: Optional[Node] = None) -> None:
        print("Behaviors Init")
       
        self.robot_name = robot_name
        self.body_frame_name = namespace_with(self.robot_name, BODY_FRAME_NAME)
        self.vision_frame_name = namespace_with(self.robot_name, VISION_FRAME_NAME)
        self.tf_listener = None  # Initialize to None

        try:
            if node is not None:
                print("Behaviors: Creating TFListenerWrapper")
                self.tf_listener = TFListenerWrapper(node)
                print("Behaviors: TFListenerWrapper created")
            else:
                print("Behaviors: Node is None")
        except Exception as e:
            print(str(e))



    def sit(self):
        try: 
            proto_goal = RobotCommandBuilder.synchro_sit_command()
            action_goal = RobotCommand.Goal()
            return action_goal, proto_goal, "sit"
        except Exception as e: 
            print(str(e))
        return None, None, ""
    
    def stand(self):
        try: 
            proto_goal = RobotCommandBuilder.synchro_stand_command()
            action_goal = RobotCommand.Goal()
            return action_goal, proto_goal, "stand"
        except Exception as e: 
            print(str(e))
        return None, None, ""



    def walk_forward(self):
        try:
            world_t_robot = self.tf_listener.lookup_a_tform_b(
                self.vision_frame_name, self.body_frame_name
            ).get_closest_se2_transform()
            world_t_goal = world_t_robot * SE2Pose(1.0, 0.0, 0.0)
            proto_goal = RobotCommandBuilder.synchro_se2_trajectory_point_command(
                goal_x=world_t_goal.x,
                goal_y=world_t_goal.y,
                goal_heading=world_t_goal.angle,
                frame_name=VISION_FRAME_NAME,  # use Boston Dynamics' frame conventions
            )
            action_goal = RobotCommand.Goal()
            return action_goal, proto_goal, "walk_forward"
        except Exception as e: 
            print(str(e))
        return None, None, ""
    
    def walk_backward(self) -> None:
        try: 
            world_t_robot = self.tf_listener.lookup_a_tform_b(
                self.vision_frame_name, self.body_frame_name
            ).get_closest_se2_transform()
            world_t_goal = world_t_robot * SE2Pose(-1.0, 0.0, 0.0)
            proto_goal = RobotCommandBuilder.synchro_se2_trajectory_point_command(
                goal_x=world_t_goal.x,
                goal_y=world_t_goal.y,
                goal_heading=world_t_goal.angle,
                frame_name=VISION_FRAME_NAME,  # use Boston Dynamics' frame conventions
            )
            action_goal = RobotCommand.Goal()
            return action_goal, proto_goal, "walk_forward"
        except Exception as e: 
            print(str(e))
        return None, None, ""
    
    
    def turn_left(self) -> None:
        try:
            print("Turning 20 degrees")
            world_t_robot = self.tf_listener.lookup_a_tform_b(
                self.vision_frame_name, self.body_frame_name
            ).get_closest_se2_transform()
            world_t_goal = world_t_robot * SE2Pose(0.0, 0.0, math.radians(20))
            print("%s",world_t_goal)
            proto_goal = RobotCommandBuilder.synchro_se2_trajectory_point_command(
                goal_x=world_t_goal.x,
                goal_y=world_t_goal.y,
                goal_heading=world_t_goal.angle,
                frame_name=VISION_FRAME_NAME,  # use Boston Dynamics' frame conventions
            )
            action_goal = RobotCommand.Goal()
            return action_goal, proto_goal, "look_for_object"
        except Exception as e: 
            print(str(e))
        return None, None, ""


class RobotControl:
    def __init__(self, robot_name: Optional[str] = None, node: Optional[Node] = None) -> None:
        self._logger = logging.getLogger(fqn(self.__class__))
        node = node or ros_scope.node()
        if node is None:
            raise ValueError("no ROS 2 node available (did you use bdai_ros2_wrapper.process.main?)")
        self._robot_name = robot_name

        # SimpleSpotCommander wraps some service clients to use spot driver services
        self._robot = SimpleSpotCommander(self._robot_name, node)
        
        # ActionClientWrapper talks to an action server in spot driver
        self._robot_command_client = ActionClientWrapper(
            RobotCommand, namespace_with(self._robot_name, "robot_command"), node
        )

        # Initialize robot behaviour class
        self.Behaviours = Behaviours(self._robot_name, node)

        # Create subscriber to listen to new incoming commands
        self.txtMsgSubscriber = node.create_subscription(String, 'txt_input', self.command_callback, 10)



    def initialize_robot(self) -> bool:
        #Claim the robot
        self._logger.info(f"Robot name: {self._robot_name}")
        self._logger.info("Claiming robot")
        result = self._robot.command("claim")
        if not result.success:
            self._logger.error("Unable to claim robot message was " + result.message)
            return False
        self._logger.info("Claimed robot")

        # Power robot on
        self._logger.info("Powering robot on")
        result = self._robot.command("power_on")
        if not result.success:
            self._logger.error("Unable to power on robot message was " + result.message)
            return False
        
        # Stand the robot up.
        self._logger.info("Standing robot up")
        result = self._robot.command("stand")
        if not result.success:
            self._logger.error("Robot did not stand message was " + result.message)
            return False
        self._logger.info("Successfully stood up.")
        return True
    

    def command_callback(self, msg):
        command = msg.data
        action_goal = None
        if command == "forward": 
            action_goal, proto_goal, action_name = self.Behaviours.walk_forward()
        elif command == "backward": 
            action_goal, proto_goal, action_name = self.Behaviours.walk_backward()
        elif command == "left": 
            action_goal, proto_goal, action_name = self.Behaviours.turn_left()
        elif command == "right": 
            action_goal, proto_goal, action_name = self.Behaviours.turn_right()
        elif command == "stop":
            self.release_robot()
            

        if action_goal is not None: 
            conv.convert_proto_to_bosdyn_msgs_robot_command(proto_goal, action_goal.command)
            self._robot_command_client.send_goal_and_wait(action_name, action_goal)


    def terminal_control(self):
        while(True):
            command = input("Choose the next robot command: \nw - move forward, s - move backward, a - turn left, d - turn right, p - sit, power off & release ) ")
            action_goal = None
            if command == "w": 
                action_goal, proto_goal, action_name = self.Behaviours.walk_forward()
            elif command == "s": 
                action_goal, proto_goal, action_name = self.Behaviours.walk_backward()
            elif command == "a": 
                action_goal, proto_goal, action_name = self.Behaviours.turn_left()
            elif command == "d": 
                action_goal, proto_goal, action_name = self.Behaviours.turn_right()
            elif command == "p":
                self.release_robot()
                break

            if action_goal is not None: 
                conv.convert_proto_to_bosdyn_msgs_robot_command(proto_goal, action_goal.command)
                self._robot_command_client.send_goal_and_wait(action_name, action_goal, timeout_sec=0.5)
               
    
    def release_robot(self):
        # Make robot sit down.
        self._logger.info("Make robot sit")
        result = self._robot.command("sit")
        time.sleep(3.0)

        if not result.success:
            self._logger.error("Robot did not sit down message was " + result.message)
            return False
        else:
            self._logger.info("Successfully sat down.")
            # Power robot off
            self._logger.info("Powering robot off")
            result = self._robot.command("power_off")
            if not result.success:
                self._logger.error("Unable to power off robot message was " + result.message)
                return False

            else:
                #Release the robot
                self._logger.info("Releasing robot")
                result = self._robot.command("release")
                if not result.success:
                    self._logger.error("Unable to release robot message was " + result.message)
                    return False
                self._logger.info("Release robot")

            return True



def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default=None)
    return parser


@ros_process.main(cli())
def main(args: argparse.Namespace) -> int:
    controller = RobotControl(args.robot, main.node)
    controller.initialize_robot()
    controller.terminal_control()


if __name__ == "__main__":
    exit(main())
