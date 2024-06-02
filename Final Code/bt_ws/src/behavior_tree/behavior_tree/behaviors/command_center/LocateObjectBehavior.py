import json
import logging
import py_trees
from py_trees.common import Status 



class LocateObject(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.known_objects = ["banana", "apple", "cup", "laptop", "dog", "cat", "bottle", "teddy bear", "person", "bowl", "refrigerator"]

        except Exception as e:
            self.logger.error(str(e))
        
    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","RED")

    def update(self) -> Status:
        try: 
            functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
            args=json.loads(functions_to_call[0].function.arguments)
            object=args["object"]
            self.logger.info("Object to look for:%s", object)
            py_trees.blackboard.Blackboard.set("locate_object_behavior", "disabled")
            py_trees.blackboard.Blackboard.set("chatgpt/function_call","")

         
            
            behavior_msg = py_trees.blackboard.Blackboard.get("ChatGPT_behavior_msg")
            if behavior_msg:
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                py_trees.blackboard.Blackboard.set("text_to_speak/locate_object",msg)
                py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
                py_trees.blackboard.Blackboard.set("chatgpt/msg","")

            else:
                py_trees.blackboard.Blackboard.set("robot_control/detect_object", object)
                py_trees.blackboard.Blackboard.set("text_to_speak/locate_object","Sure, i will look for "+str(object))
        
            return py_trees.common.Status.SUCCESS
        
        except Exception as e:
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE  

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
    