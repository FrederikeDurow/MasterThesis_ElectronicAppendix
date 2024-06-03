#!/usr/bin/env python
import math
import logging
import rclpy
#from spot_msgs.action import RobotCommand
#import bdai_ros2_wrappers.scope as ros_scope
from bosdyn.client.math_helpers import Quat, SE3Pose
from bosdyn.client.robot_command import RobotCommandBuilder
#from bdai_ros2_wrappers.tf_listener_wrapper import TFListenerWrapper
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
from bosdyn.api import geometry_pb2
from bosdyn.api import geometry_pb2 as geo
#from bdai_ros2_wrappers.utilities import namespace_with
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, VISION_FRAME_NAME
from bosdyn import geometry
from rclpy.node import Node
#from spot_examples.simple_spot_commander import SimpleSpotCommander


class Behaviours(Node):
    def __init__(self, node: ros_scope.node(), robot_name, logger: logging.Logger) -> None:
        try: 
            self.logger = logger
            self.robot_name = robot_name
            self.node =node
            self._robot = SimpleSpotCommander(self.robot_name,self.node)
            self.body_frame_name = namespace_with(self.robot_name, BODY_FRAME_NAME)
            self.vision_frame_name = namespace_with(self.robot_name, VISION_FRAME_NAME)    
            self.tf_listener = TFListenerWrapper()

        except Exception as e:
            self.logger.error(str(e))


    def sit(self):
        try: 
            proto_goal = RobotCommandBuilder.synchro_sit_command()
            action_goal = RobotCommand.Goal()
            return [action_goal], [proto_goal], "Sit"
        except Exception as e: 
            self.logger.error(str(e))
        return None, None, ""
    
    def stand(self):
        try: 
            proto_goal = RobotCommandBuilder.synchro_stand_command()
            action_goal = RobotCommand.Goal()
        
            return [action_goal], [proto_goal], "Stand"
        except Exception as e: 
            self.logger.error(str(e))
        return None, None, ""

    def power_off(self):
        try: 
            proto_goal = RobotCommandBuilder.safe_power_off_command()
            action_goal = RobotCommand.Goal()
            return [action_goal], [proto_goal], "Power Off"
        except Exception as e: 
            self.logger.error(str(e))
        return None, None, ""
    
    def initialize(self):
        try: 
            result = self._robot.command("claim")
            if not result.success:
                self.logger.error("Unable to claim robot message was " + result.message)
                return None, None, "" # False
            
            result = self._robot.command("power_on")
            if not result.success:
                self.logger.error("Unable to power on robot message was " + result.message)
                return None, None, "" # False

        except Exception as e: 
            self.logger.error(str(e))
        return None, None, "" #True


    def look_for_object(self): 
        try: 
            action_goals = []
            proto_goals = []
            rotations = []
            # original_position
            r = geometry.EulerZXY(yaw=math.radians(0), pitch=-math.radians(0))
            rotations.append(r)
            # left_down
            r = geometry.EulerZXY(yaw=math.radians(45), pitch=math.radians(45))
            rotations.append(r)
            # middle1_down 
            r = geometry.EulerZXY(yaw=math.radians(15), pitch=math.radians(45))
            rotations.append(r)
            # middle2_down 
            r = geometry.EulerZXY(yaw=-math.radians(15), pitch=math.radians(45))
            rotations.append(r)
            # right_down
            r = geometry.EulerZXY(yaw=-math.radians(45), pitch=math.radians(45))
            rotations.append(r)
            
            # original_position
            r = geometry.EulerZXY(yaw=math.radians(0), pitch=-math.radians(0))
            rotations.append(r)
          
            for r in rotations: 
                proto_goal = RobotCommandBuilder.synchro_stand_command(footprint_R_body=r) 
                proto_goals.append(proto_goal)
                action_goals.append(RobotCommand.Goal())
            return action_goals, proto_goals, "Look For Object"


        except Exception as e: 
            self.logger.error(str(e))
        return None, None, ""
    

    def talk(self): 
        try: 
            action_goals = []
            proto_goals = []
            rotations = []
            for _ in range(3):
                # left
                r = geometry.EulerZXY(yaw=math.radians(5))
                rotations.append(r)
                # right
                r = geometry.EulerZXY(yaw=-math.radians(5))
                rotations.append(r)
            r = geometry.EulerZXY(yaw=math.radians(0), pitch=-math.radians(0))
            rotations.append(r)
            
            for r in rotations: 
                proto_goal = RobotCommandBuilder.synchro_stand_command(footprint_R_body=r)
                proto_goals.append(proto_goal)
                action_goals.append(RobotCommand.Goal())
            return action_goals, proto_goals, "Talking"


        except Exception as e: 
            self.logger.error(str(e))
        return None, None, ""



def main(args=None):
    rclpy.init(args=args)
    behaviours = Behaviours()
    rclpy.spin(behaviours)
    behaviours.destroy_node()
    rclpy.shutdown()
        

