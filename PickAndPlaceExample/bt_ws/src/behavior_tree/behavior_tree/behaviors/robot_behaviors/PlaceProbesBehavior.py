# import logging
# import py_trees
# from std_msgs.msg import String
# from py_trees.common import Status

# class PlaceProbes(py_trees.behaviour.Behaviour):
#     def __init__(self, name: str, logger: logging.Logger):
#         super().__init__(name=name)
#         self.logger = logger
       
#     def setup(self, **kwargs) -> None:
#         try:
#             self.node = kwargs['node']
#         except KeyError as e:
#             error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
#             raise KeyError(error_message) from e  
#         self.all_labels = []

   
#     def initialise(self) -> None:
#         try: 
#             self.brand = py_trees.blackboard.Blackboard.get("place_probes/brand")

#             if self.brand is not None:
#                 conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
#                 function_id = py_trees.blackboard.Blackboard.get("function_id")
#                 msg={
#                         "role": "function",
#                         "tool_call_id": function_id,
#                         "name": "place_probes",
#                         "content":"[FAILURE]: The probes, could not be placed.",
#                         }
#                 conversation.append(msg)
#                 py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
#             self.nr_of_probes = py_trees.blackboard.Blackboard.get("place_probes/number")
#             self.count = 0
#         except Exception as e: 
#             self.logger.error(str(e))
        

#     def update(self) -> Status:
#         try:
#             # Start Robot 
#             if self.count < self.nr_of_probes: # Check if robot still running
                
#                 self.count+=1
#                 self.logger.info(str(self.count))
#                 return py_trees.common.Status.RUNNING 

#             else: 
#                     conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
#                     function_id = py_trees.blackboard.Blackboard.get("function_id")
#                     msg={
#                         "role": "function",
#                         "tool_call_id": function_id,
#                         "name": "place_probes",
#                         "content":"[SUCCESS]: The probes were successfully placed in the fridge.",
#                         }
#                     conversation.pop()
#                     conversation.append(msg)
#                     py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)      
#                     return py_trees.common.Status.SUCCESS       
              

#         except Exception as e: 
#             self.logger.error(str(e))
#             return py_trees.common.Status.FAILURE


#     def terminate(self, new_status: Status) -> None:
#         # Stop Robot  
#         return super().terminate(new_status)

# import logging
# import py_trees
# import cv2
# import os

# import numpy as np
# from std_msgs.msg import String
# from py_trees.common import Status
# import time
# os.environ["QT_QPA_PLATFORM"] = "offscreen"

# class PlaceProbes(py_trees.behaviour.Behaviour):
#     def __init__(self, name: str, logger: logging.Logger):
#         super().__init__(name=name)
#         self.logger = logger
#         self.window_name = 'Probes Display'
#         self.robot_image = cv2.imread("/home/frederike/Documents/Speciale/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/behaviors/robot_behaviors/robot.png")
#         self.robot_probe_image = cv2.imread("/home/frederike/Documents/Speciale/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/behaviors/robot_behaviors/robot_with_probe.png")

#     def setup(self, **kwargs) -> None:
#         try:
#             self.node = kwargs['node']
#         except KeyError as e:
#             error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
#             raise KeyError(error_message) from e  
#         self.all_labels = []

#     def initialise(self) -> None:
#         try: 
#             self.nr_of_probes = py_trees.blackboard.Blackboard.get("place_probes/number")

#             if self.nr_of_probes is not None:
#                 conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
#                 function_id = py_trees.blackboard.Blackboard.get("function_id")
#                 msg={
#                         "role": "function",
#                         "tool_call_id": function_id,
#                         "name": "place_probes",
#                         "content":"[FAILURE]: The probes, could not be placed.",
#                         }
#                 conversation.append(msg)
#                 py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
#             self.count = 0
#             cv2.namedWindow(self.window_name)
#         except Exception as e: 
#             self.logger.error(str(e))
        
#     def update(self) -> Status:
#         try:
#             if self.count < self.nr_of_probes: 
#                 cv2.imshow(self.window_name, self.robot_image)
#                 cv2.waitKey(1000)
            
#                 cv2.imshow(self.window_name, self.robot_probe_image)
#                 cv2.waitKey(1000)  # Display each image for 1 second

#                 self.count += 1
#                 self.logger.info(str(self.count))
#                 return py_trees.common.Status.RUNNING 
#             else: 
#                 conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
#                 function_id = py_trees.blackboard.Blackboard.get("function_id")
#                 msg = {
#                     "role": "function",
#                     "tool_call_id": function_id,
#                     "name": "place_probes",
#                     "content":"[SUCCESS]: The probes were successfully placed in the fridge.",
#                     }
#                 conversation.pop()
#                 conversation.append(msg)
#                 py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
                
#                 cv2.destroyWindow(self.window_name)
#                 return py_trees.common.Status.SUCCESS       
#         except Exception as e: 
#             self.logger.error(str(e))
#             cv2.destroyWindow(self.window_name)
#             return py_trees.common.Status.FAILURE

#     def terminate(self, new_status: Status) -> None:
#         cv2.destroyWindow(self.window_name)
#         return super().terminate(new_status)


import logging
import py_trees
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from std_msgs.msg import String
from py_trees.common import Status
import time

class PlaceProbes(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
        self.window_name = 'Probes Display'
        self.robot_image_path = "/home/frederike/Documents/Speciale/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/behaviors/robot_behaviors/robot.png"
        self.robot_probe_image_path = "/home/frederike/Documents/Speciale/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/behaviors/robot_behaviors/robot_with_probe.jpg"

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name, e)
            raise KeyError(error_message) from e  
        self.all_labels = []

    def initialise(self) -> None:
        try: 
            self.nr_of_probes = py_trees.blackboard.Blackboard.get("place_probes/number")*2

            if self.nr_of_probes is not None:
                conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                function_id = py_trees.blackboard.Blackboard.get("function_id")
                msg = {
                    "role": "function",
                    "tool_call_id": function_id,
                    "name": "place_probes",
                    "content":"[FAILURE]: The probes, could not be placed.",
                }
                conversation.append(msg)
                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
            self.count = 0
            self.fig, self.ax = plt.subplots()
            plt.ion()  # Turn on interactive mode
            plt.show()
        except Exception as e: 
            self.logger.error(str(e))
        
    def update(self) -> Status:
        try:
            if self.count < self.nr_of_probes: 
                if self.count % 2 == 0:
                    image = mpimg.imread(self.robot_image_path)
                else:
                    image = mpimg.imread(self.robot_probe_image_path)

                self.ax.imshow(image)
                self.fig.canvas.draw()
                plt.pause(1)  # Display each image for 1 second

                self.count += 1
                self.logger.info(str(self.count))
                return py_trees.common.Status.RUNNING 
            else: 
                plt.close('all')
                conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                function_id = py_trees.blackboard.Blackboard.get("function_id")
                msg = {
                    "role": "function",
                    "tool_call_id": function_id,
                    "name": "place_probes",
                    "content":"[SUCCESS]: The probes were successfully placed in the fridge.",
                }
                conversation.pop()
                conversation.append(msg)
                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
                
                return py_trees.common.Status.SUCCESS       
        except Exception as e: 
            self.logger.error(str(e))
            plt.close(self.fig)
            return py_trees.common.Status.FAILURE

    def terminate(self, new_status: Status) -> None:
        plt.close(self.fig)
        return super().terminate(new_status)
