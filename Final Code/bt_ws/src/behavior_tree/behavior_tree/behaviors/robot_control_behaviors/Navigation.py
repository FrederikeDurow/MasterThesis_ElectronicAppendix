import logging
import py_trees
from py_trees.common import Status
from rclpy.duration import Duration
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import Odometry
import yaml


class Navigation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger= logger

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.subscription = self.node.create_subscription(Odometry,'/odometry',self.odom_callback,10) # maybe /odom
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e
        try:
            self.navigator = BasicNavigator()
            self.navigator.lifecycleStartup()
        except Exception as e:
            self.logger.error(str(e))

    def initialise(self) -> None:
        self.task_started = False
        self.navigation_stopped = False
        self.nav_start = None
        py_trees.blackboard.Blackboard.set("LED_COLOR","RED")
        ###
        self.regions = yaml.safe_load("bt_ws/src/behavior_tree/behavior_tree/config/regions.yaml")
        self.goal_area = py_trees.blackboard.Blackboard.get("goal_area")


    def update(self) -> Status:
        try:
            if self.task_started is False:
                py_trees.blackboard.Blackboard.set("LED_COLOR", "RED")
                goal_poses = py_trees.blackboard.Blackboard.get("robot_control/goal_poses")
                self.nav_start = self.navigator.get_clock().now()
                self.navigator.followWaypoints(goal_poses)
                self.task_started = True
            
            else:
                if not self.navigator.isTaskComplete():
                    now = self.navigator.get_clock().now()
                    if now - self.nav_start > Duration(seconds=180.0):
                        self.navigator.cancelTask()
                        self.navigation_stopped = True
                        
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        function_id = py_trees.blackboard.Blackboard.get("function_id")
                        msg={
                                "role": "function",
                                "tool_call_id": function_id,
                                "name": "go_to_area",
                                "content":"[FAILURE]: Navigating to the "+str(self.goal_area)+" failed due to timeout in the Nav2 algorithm. ",
                                }
                        conversation.append(msg)
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
                        self.logger.info("Task cancled because of timeout.")
                        return py_trees.common.Status.SUCCESS
                else:
                    self.navigation_stopped = True
                
                if self.navigation_stopped == True:
                    result = self.navigator.getResult()
                    self.logger.info("result: %s", result)

                    if result == TaskResult.SUCCEEDED:
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        function_id = py_trees.blackboard.Blackboard.get("function_id")
                        msg={
                                "role": "function",
                                "tool_call_id": function_id,
                                "name": "go_to_area",
                                "content":"[SUCCESS]: Navigating to " +str(self.goal_area)+ " has been completed successfully. ",
                                }
                        conversation.append(msg)
                        py_trees.blackboard.Blackboard.set("current_location",self.goal_area)
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
                        return py_trees.common.Status.SUCCESS
                    
                    elif result == TaskResult.FAILED:
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        function_id = py_trees.blackboard.Blackboard.get("function_id")

                        if self.check_if_region() is not None:
                            current_location = self.check_if_region()
                            if current_location == self.goal_area:
                                msg={
                                        "role": "function",
                                        "tool_call_id": function_id,
                                        "name": "go_to_area",
                                        "content":"[WARNING]: Navigating to the center of "+str(self.goal_area)+" has been completed unsuccessfully, but i managed to get to a place within "+str(self.goal_area),
                                    }
                                conversation.append(msg)
                                py_trees.blackboard.Blackboard.set("current_location",self.goal_area)
                                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
                                self.logger.warning("Navigation warning!")
                            else:
                                msg={
                                        "role": "function",
                                        "tool_call_id": function_id,
                                        "name": "go_to_area",
                                        "content":"[FAILED]: Navigating to "+str(self.goal_area)+" has been completed unsuccessfully. Current location is: "+str(current_location),
                                    }
                                conversation.append(msg)
                                py_trees.blackboard.Blackboard.set("current_location",current_location)
                                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
                        else:
                            msg={
                                    "role": "function",
                                    "tool_call_id": function_id,
                                    "name": "go_to_area",
                                    "content":"[FAILED]: Navigating to "+str(self.goal_area)+" has been completed unsuccessfully. Currently not in any regions that its known",
                                }
                            conversation.append(msg)
                            py_trees.blackboard.Blackboard.set("current_location",None)
                            py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)    

                        return py_trees.common.Status.SUCCESS
                    else:
                        self.logger.warning("Navigation: Invalid return status.")

        except Exception as e:
            self.logger.error(str(e))
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.RUNNING


    def terminate(self, new_status: Status) -> None:
        self.navigator.cancelTask()
        return super().terminate(new_status)
    

    def odom_callback(self, msg:Odometry):
        self.position = (msg.pose.pose.position.x, msg.pose.pose.position.y)

    def check_if_region(self):

        if self.position is None:
            return None
        
        else:
            x, y = self.position
            for region, info in self.regions.items():
                vertices = info['vertices']
                if self.point_inside_polygon(x, y, vertices):
                    return region

            return None

    def point_inside_polygon(self, x, y, vertices):
        n = len(vertices)
        inside = False

        p1x, p1y = vertices[0]['x'], vertices[0]['y']
        for i in range(n + 1):
            p2x, p2y = vertices[i % n]['x'], vertices[i % n]['y']
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    