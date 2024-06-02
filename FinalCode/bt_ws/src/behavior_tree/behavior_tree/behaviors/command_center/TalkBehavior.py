import logging
import py_trees
from py_trees.common import Status 


class TalkToOperator(py_trees.behaviour.Behaviour):
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
        py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW") 
        py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "disabled")
        py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
        py_trees.blackboard.Blackboard.set("ChatGPT_active", True)

        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
 