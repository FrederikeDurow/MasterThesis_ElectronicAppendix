from spot_wrapper.wrapper import SpotDance

import json
import os
import py_trees
import logging
from py_trees.common import Status 
from geometry_msgs.msg import PoseStamped
from behavior_tree.config.chatgpt_tools import TOOLS


class PerformMovementBehavior(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        
    def initialise(self) -> None:
        pass

    def update(self) -> Status:
        try:
            functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
            args=json.loads(functions_to_call[0].function.arguments)
            move=args["move"]
            py_trees.blackboard.Blackboard.set("text_to_speak/perform_move","Sure, i will perform "+str(args["move"]))

            #self.go_to_area(goal_area,go_through_area)
            py_trees.blackboard.Blackboard.set("go_to_area_behavior", "disabled")
            py_trees.blackboard.Blackboard.set("chatgpt/function_call","")
            return py_trees.common.Status.SUCCESS 
        except Exception as e:
            self.logger.error("No behavior enabled because of exception: %s", e)
        
        return py_trees.common.Status.FAILURE

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)