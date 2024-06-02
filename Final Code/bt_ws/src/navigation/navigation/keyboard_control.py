#!/usr/bin/env python
# Our own keyboard control script based on spot_ros
# because wasd.py isn't compatible with the spot_ros
# driver setup.
#
# This function 'synchro_se2_trajectory_point_command' is useful too.
# https://github.com/boston-dynamics/spot-sdk/blob/master/python/bosdyn-client/src/bosdyn/client/robot_command.py#L851
import time
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from rbd_spot.utils.keys import getch
from std_msgs.msg import String
import argparse

TRANS_VEL = 0.5    # m/s
ROT_VEL = 0.5    # rad/s

class Move:
    def __init__(self, name, vtrans=(0.0, 0.0, 0.0), vrot=(0.0, 0.0, 0.0)):
        """
        Args:
            name (str): name of movement
            vtrans (tuple): (vx, vy, vz) translational velocity
            vrot (tuple): (vx, vy, vz) rotational velocity

        The geometry of Spot coordinates is documented here:
        https://dev.bostondynamics.com/docs/concepts/geometry_and_frames
        """
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
    """
    Args:
        key (str): character of the key currently pressed
        curtime (time): time of key pressed
        last_key (str): character of the last key pressed
        last_time (time): time of last key pressed
        hold_time_gap (float): the amount of time between two getch() event-returns
            when one is actually holding a key. This is used to identify whether
            a user is holding the key. This is typically < 0.3.
    """
    if key == last_key:
        if cur_time - last_time < hold_time_gap:
            return True
    return False

    
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

class KeyPublisher(Node):

    _move = Move()

    def __init__(self):
        super().__init__('spot_keyboard_control')
        self.publisher_ = self.create_publisher(String, '/spot/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main():
    keyboardpublisher = KeyPublisher()
    rclpy.spin(keyboardpublisher)

    controls = {
        "w": Move("forward", vtrans=(TRANS_VEL, 0.0, 0.0)),
        "a": Move("left", vtrans=(0.0, TRANS_VEL, 0.0)),
        "d": Move("right", vtrans=(0.0, -TRANS_VEL, 0.0)),
        "s": Move("back", vtrans=(-TRANS_VEL, 0.0, 0.0)),
        "q": Move("turn_left", vrot=(0.0, 0.0, ROT_VEL)),
        "e": Move("turn_right", vrot=(0.0, 0.0, -ROT_VEL)),
        "p": release_robot()
    }
    print_controls(controls)

    _start_time = time.time()

    _last_key = None
    _last_time = None

    while True:
        k = getch()
        if k == "c":
            print("bye.")
            break

        if k == "h":
            print_controls(controls)

        if k in controls:
            action = controls[k]
            key_time = time.time() - _start_time
            # We only publish the message when the user is holding the key
            if _last_key is not None:
                if is_holding(k, key_time, _last_key, _last_time):
                    m = action.to_message()
                    pub.publish(m)
                    print("%.3fs: holding %s" % (key_time, action.name))
                else:
                    print("%.3fs: pressed %s" % (key_time, action.name))
            _last_key = k
            _last_time = key_time
        max_rate.sleep()

    rclpy.shutdown()


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default=None)
    return parser



if __name__ == "__main__":
    exit(main())
