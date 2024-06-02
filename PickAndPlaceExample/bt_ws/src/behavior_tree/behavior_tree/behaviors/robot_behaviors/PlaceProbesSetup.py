import logging
import json
import py_trees
from py_trees.common import Status 


class PlaceProbesSetup(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except Exception as e:
            self.logger.error(str(e))
       
    def initialise(self) -> None:
        pass

    def update(self) -> Status:
        # get function information 
        functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
        args=json.loads(functions_to_call[0].function.arguments)
        
        number_of_probes=args["number_of_probes"]
        py_trees.blackboard.Blackboard.set("place_probes/number", number_of_probes)

        behavior_msg = py_trees.blackboard.Blackboard.get("ChatGPT_behavior_msg")
        if behavior_msg:
            msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
            py_trees.blackboard.Blackboard.set("text_to_speak/place_probes",msg)
            py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
            py_trees.blackboard.Blackboard.set("chatgpt/msg","")

        else:
            py_trees.blackboard.Blackboard.set("text_to_speak/place_probes","Sure, I will place the "+str(number_of_probes)+ " probes.")
               
        py_trees.blackboard.Blackboard.set("place_probes_behavior", "disabled")
        py_trees.blackboard.Blackboard.set("chatgpt/function_call","")


        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
 
