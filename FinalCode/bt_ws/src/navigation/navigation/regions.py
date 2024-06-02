''' ####################
    Publish (x,y) coordinate goals for a differential drive robot in a 
    Gazebo maze.
    ==================================
    Author: Addison Sears-Collins
    Date: November 21, 2020
    #################### '''
  
import rclpy # Import the ROS client library for Python
from rclpy.node import Node # Enables the use of rclpy's Node class
from std_msgs.msg import Float64MultiArray # Enable use of std_msgs/Float64MultiArray message
from geometry_msgs.msg import PoseStamped
  
class GoalPublisher(Node):
  """
  Create a GoalPublisher class, which is a subclass of the Node class.
  The class publishes the goal positions (x,y) for a mobile robot in a Gazebo maze world.
  """
   
  def __init__(self):
    """
    Class constructor to set up the node
    """
    
    # Initiate the Node class's constructor and give it a name
    super().__init__('goal_publisher')
      
    # Create publisher(s)      
    self.publisher_goal_value = self.create_publisher(PoseStamped, '/goal_pose', 10)

    # [x,y,w]
    self.MapRegions ={
        "kitchen": [4.123695373535156,-2.4020678997039795],
        "office": [5.491644382476807,2.7653961181640625],
        "garage": [4.757437705993652,9.010248184204102]
}
    
  def publish_goal_point(self, region:str):
    """
    Callback function.
    """
    if region.lower() in self.MapRegions:
        goal=self.MapRegions[region]
        msg=PoseStamped()
        msg.pose.position.x=goal[0]
        msg.pose.position.y=goal[1]
        msg.pose.position.z=0.0
        msg.pose.orientation.w=1.0
        self.publisher_goal_value.publish(msg)
    else:
      pass
      
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  goal_publisher = GoalPublisher()
  goal_publisher.publish_goal_point("kitchen")
  
  # Spin the node so the callback function is called.
  # Publish any pending messages to the topics.
  rclpy.spin(goal_publisher)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  goal_publisher.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()



##Kitchen
#---
#header:
#  stamp:
#    sec: 1707748872
#    nanosec: 958986195
#  frame_id: map
#point:
#  x: 4.123695373535156
#  y: -2.4020678997039795
#  z: 0.0033121109008789062
#---
##Office
#---
#header:
#  stamp:
#    sec: 1707748929
#    nanosec: 217645992
#  frame_id: map
#point:
#  x: 5.491644382476807
#  y: 2.7653961181640625
#  z: 0.0010843276977539062
#---
##Garage
#---
#header:
#  stamp:
#    sec: 1707749051
#    nanosec: 663577522
#  frame_id: map
#point:
#  x: 4.757437705993652
#  y: 9.010248184204102
#  z: -0.0011262893676757812
#---



