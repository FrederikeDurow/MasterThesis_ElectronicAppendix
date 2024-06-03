import py_trees
import logging
from py_trees.common import Status
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration


class Navigation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger= logger
       
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  
        try: 
            self.navigator = BasicNavigator()
            self.navigator.lifecycleStartup()
        except Exception as e: 
            self.logger.error(str(e))

    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","RED")
        self.goal_area = py_trees.blackboard.Blackboard.get("goal_area")

    def update(self) -> Status:
        try:
            self.logger.info("NAVIGATION CALLED: SIMULATE SUCCESS")
            conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
            function_id = py_trees.blackboard.Blackboard.get("function_id")
            msg={
                    "role": "function",
                    "tool_call_id": function_id,
                    "name": "go_to_area",
                    "content":"[SUCCESS]: Navigating to " +str(self.goal_area)+ " has been completed successfully.",
                }
            conversation.append(msg)
            py_trees.blackboard.Blackboard.set("current_location",self.goal_area)
            py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
            return py_trees.common.Status.SUCCESS
                
        except Exception as e: 
            self.logger.error(str(e))
        py_trees.blackboard.Blackboard.set("text_to_speak/go_to_area/done","Unfortunately I could not reach the goal location.")
        return py_trees.common.Status.FAILURE 

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

