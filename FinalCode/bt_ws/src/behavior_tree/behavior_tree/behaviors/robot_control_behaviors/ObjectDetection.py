import logging
import py_trees
from std_msgs.msg import String
from py_trees.common import Status

class ObjectDetection(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
       
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  
        self.all_labels = []

        self.object = ""
        self.found_object = False
        self.labelSubscriber = self.node.create_subscription(String, 'object_labels', self.label_callback, 10)
      
    
    
    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("object_found","False")   
        self.object = py_trees.blackboard.Blackboard.get("robot_control/detect_object")
        self.logger.info("Looking for: %s",self.object)
        if self.object is not None:
            conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
            function_id = py_trees.blackboard.Blackboard.get("function_id")
            msg={
                    "role": "function",
                    "tool_call_id": function_id,
                    "name": "locate_object",
                    "content":"[FAILURE]: The desired object,"+str(self.object)+", was not found. ",
                    }
            conversation.append(msg)
            py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
        self.found_object = False
        

    def update(self) -> Status:
        try:
            if self.object is not None:
                py_trees.blackboard.Blackboard.set("LED_COLOR", "RED")
                

                if self.found_object:
                    conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                    function_id = py_trees.blackboard.Blackboard.get("function_id")
                    msg={
                        "role": "function",
                        "tool_call_id": function_id,
                        "name": "locate_object",
                        "content":"[SUCCESS]: The desired object,"+str(self.object)+", was found.",
                        }
                    conversation.pop()
                    conversation.append(msg)
                    py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)      
                    py_trees.blackboard.Blackboard.set("object_found",True)      
                    return py_trees.common.Status.SUCCESS          

        except Exception as e: 
            self.logger.error(str(e))

            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.RUNNING

    def label_callback(self, msg: String) -> None:
        if msg.data == self.object:
            self.found_object = True

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

