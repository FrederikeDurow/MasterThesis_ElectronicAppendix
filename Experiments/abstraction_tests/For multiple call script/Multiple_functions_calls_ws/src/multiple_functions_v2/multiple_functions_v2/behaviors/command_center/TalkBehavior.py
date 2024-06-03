import py_trees
import logging
from py_trees.common import Status 
# Put correct sentence on blackboard if necessary
# Disable behavior

class TalkToOperator(py_trees.behaviour.Behaviour):
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
        py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW") 
        py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "disabled")
        # # Remapping ChatGpt msg to Speech Synthesizer msg
        # msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
        # py_trees.blackboard.Blackboard.set("text_to_speak/talk", msg)
        py_trees.blackboard.Blackboard.set("STT_flag", True)
        py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
        # py_trees.blackboard.Blackboard.set("first_run", False)
        py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
 

    def main(self):
        py_trees.blackboard.Blackboard.set("text_to_speak/talk", "Hey, I am spot. This is a test.")

if __name__ == '__main__':
    talk = TalkToOperator()
    talk.main()