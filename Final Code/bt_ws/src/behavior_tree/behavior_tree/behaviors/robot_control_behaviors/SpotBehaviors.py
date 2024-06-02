#!/usr/bin/env python
import math
import logging
import rclpy
import bdai_ros2_wrappers.scope as ros_scope
from rclpy.node import Node

from spot_msgs.action import RobotCommand
from bosdyn import geometry
from bosdyn.client.robot_command import RobotCommandBuilder


class Behaviours(Node):
    def __init__(self, node: ros_scope.node(), robot_name, logger: logging.Logger) -> None:
        try: 
            self.logger = logger
            self.robot_name = robot_name
            self.node =node

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
            # left
            r = geometry.EulerZXY(yaw=math.radians(2.5))
            rotations.append(r)
            # right
            r = geometry.EulerZXY(yaw=-math.radians(2.5))
            rotations.append(r)
            # middle
            r = geometry.EulerZXY(yaw=math.radians(0), pitch=-math.radians(2.5))
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
        

