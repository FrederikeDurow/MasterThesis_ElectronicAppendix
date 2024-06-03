import json
from geometry_msgs.msg import PoseStamped
import py_trees
import yaml
from py_trees.common import Status 
import os
import logging


class LocateObject(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.known_objects = ["person",        "bicycle",      "car",           "motorbike",     "aeroplane",   "bus",         "train",       "truck",        "boat",
            "traffic light", "fire hydrant", "stop sign",     "parking meter", "bench",       "bird",        "cat",         "dog",          "horse",
            "sheep",         "cow",          "elephant",      "bear",          "zebra",       "giraffe",     "backpack",    "umbrella",     "handbag",
            "tie",           "suitcase",     "frisbee",       "skis",          "snowboard",   "sports ball", "kite",        "baseball bat", "baseball glove",
            "skateboard",    "surfboard",    "tennis racket", "bottle",        "wine glass",  "cup",         "fork",        "knife",        "spoon",
            "bowl",          "banana",       "apple",         "sandwich",      "orange",      "broccoli",    "carrot",      "hot dog",      "pizza",
            "donut",         "cake",         "chair",         "sofa",          "pottedplant", "bed",         "diningtable", "toilet",       "tvmonitor",
            "laptop",        "mouse",        "remote",        "keyboard",      "cell phone",  "microwave",   "oven",        "toaster",      "sink",
            "refrigerator",  "book",         "clock",         "vase",          "scissors",    "teddy bear",  "hair drier",  "toothbrush"]

        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        
    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","RED")

    def update(self) -> Status:
        try: 
            functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
            args=json.loads(functions_to_call[0].function.arguments)
            object=args["object"]
            # object = py_trees.blackboard.Blackboard.get("robot_control/detect_object")
            self.logger.info("Object to look for:%s", object)
            # Reset BB variables
            py_trees.blackboard.Blackboard.set("locate_object_behavior", "disabled")
            py_trees.blackboard.Blackboard.set("chatgpt/function_call","")

            # if object in self.known_objects:
            #     py_trees.blackboard.Blackboard.set("robot_control/detect_object", object)
            #     py_trees.blackboard.Blackboard.set("text_to_speak/locate_object","Sure, i will look for "+str(object))
            # else: 
            #     py_trees.blackboard.Blackboard.set("robot_control/detect_object", None)
            #     py_trees.blackboard.Blackboard.set("text_to_speak/locate_object","Sorry, I do not know how a "+str(object)+ "looks")
            
            ###
            
            behavior_msg = py_trees.blackboard.Blackboard.get("ChatGPT_behavior_msg")
            if behavior_msg:
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                py_trees.blackboard.Blackboard.set("text_to_speak/locate_object",msg)
                py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
                py_trees.blackboard.Blackboard.set("chatgpt/msg","")

            else:
                if object in self.known_objects:
                    py_trees.blackboard.Blackboard.set("robot_control/detect_object", object)
                    py_trees.blackboard.Blackboard.set("text_to_speak/locate_object","Sure, i will look for "+str(object))
                else:
                    py_trees.blackboard.Blackboard.set("robot_control/detect_object", None) 
                    py_trees.blackboard.Blackboard.set("text_to_speak/locate_object","Sorry, I do not know how a "+str(object)+ "looks")
                    py_trees.common.Status.FAILURE 
            
            ###
            self.logger.info("ACTIVATES THE LOCATE")
            return py_trees.common.Status.SUCCESS
        
        except Exception as e:
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE  

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
    