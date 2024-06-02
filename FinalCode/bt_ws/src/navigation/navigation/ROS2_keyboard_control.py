import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from rclpy.qos import QoSProfile
import argparse

import bdai_ros2_wrappers.process as ros_process
import bdai_ros2_wrappers.scope as ros_scope
from bdai_ros2_wrappers.action_client import ActionClientWrapper
from bdai_ros2_wrappers.utilities import fqn, namespace_with
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, VISION_FRAME_NAME
from bosdyn.client.math_helpers import SE2Pose
from bosdyn.client.robot_command import RobotCommandBuilder

from keys import getch

import spot_driver.conversions as conv
from spot_msgs.action import RobotCommand  # type: ignore

TRANS_VEL = 0.5    # m/s
ROT_VEL = 0.5    # rad/s

class Move:
    def __init__(self, name, vtrans=(0.0, 0.0, 0.0), vrot=(0.0, 0.0, 0.0)):
        self.name = name
        self.vtrans = vtrans
        self.vrot = vrot

    def to_message(self):
        m = Twist()
        tx, ty, tz = self.vtrans
        m.linear.x = tx
        m.linear.y = ty
        m.linear.z = tz
        rx, ry, rz = self.vrot
        m.angular.x = rx
        m.angular.y = ry
        m.angular.z = rz
        return m

def print_controls(controls):
    print("Controls:")
    for k in controls:
        print(f"[{k}]  [{controls[k].name}]")
    print("\n[h] help")
    print("[c]  quit\n")

def is_holding(key, cur_time, last_key, last_time, hold_time_gap=0.3):
    if key == last_key:
        if cur_time - last_time < hold_time_gap:
            return True
    return False

class SpotController(Node):
    def __init__(self):
        super().__init__('spot_controller')
        self.publisher_ = self.create_publisher(Twist, '/spot/cmd_vel', QoSProfile(depth=10))
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = TRANS_VEL
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Twist message')

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

def main(args=None):
    rclpy.init(args=args)

    spot_controller = SpotController()
    spot_controller.initialize_robot()

    controls = {
        "w": Move("forward", vtrans=(TRANS_VEL, 0.0, 0.0)),
        "a": Move("left", vtrans=(0.0, TRANS_VEL, 0.0)),
        "d": Move("right", vtrans=(0.0, -TRANS_VEL, 0.0)),
        "s": Move("back", vtrans=(-TRANS_VEL, 0.0, 0.0)),
        "q": Move("turn_left", vrot=(0.0, 0.0, ROT_VEL)),
        "e": Move("turn_right", vrot=(0.0, 0.0, -ROT_VEL)),
     # Assuming release_robot is a function to release the robot
    }
    print_controls(controls)

    last_key = None
    last_time = None
    start_time = time.time()

    while rclpy.ok():
        k = getch()

        if k == "p":
            spot_controller.release_robot()
            print("bye.")
            break

        if k == "h":
            print_controls(controls)

        if k in controls:
            action = controls[k]
            key_time = time.time() - start_time

            if last_key is not None:
                if is_holding(k, key_time, last_key, last_time):
                    m = action.to_message()
                    spot_controller.publisher_.publish(m)
                    print("%.3fs: holding %s" % (key_time, action.name))
                else:
                    print("%.3fs: pressed %s" % (key_time, action.name))
            last_key = k
            last_time = key_time

    spot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default=None)
    args = parser.parse_args()
    main(args)