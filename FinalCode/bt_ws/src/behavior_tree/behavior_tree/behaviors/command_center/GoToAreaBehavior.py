import json
from geometry_msgs.msg import PoseStamped
import py_trees
import yaml
from py_trees.common import Status 
import os
import logging


class GoToArea(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        current_path = os.getcwd()
        regions_path = os.path.join(current_path, "src/behavior_tree/behavior_tree/config/regions.yaml")
        self.regions = self.load_regions_from_yaml(regions_path)

    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","RED")

    def update(self) -> Status:
        try: 
            functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
            args=json.loads(functions_to_call[0].function.arguments)
            goal_area=args["goal_area"]
            try:
                go_through_area=args["go_through_areas"]
            except:
                go_through_area=None
        
        
            behavior_msg = py_trees.blackboard.Blackboard.get("ChatGPT_behavior_msg")
            if behavior_msg:
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                py_trees.blackboard.Blackboard.set("text_to_speak/go_to_area",msg)
                behavior_msg = py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
                py_trees.blackboard.Blackboard.set("chatgpt/msg","")
            else:
                py_trees.blackboard.Blackboard.set("text_to_speak/go_to_area","Sure, i will go to "+str(args["goal_area"]))
        

            self.go_to_area(goal_area,go_through_area)
            py_trees.blackboard.Blackboard.set("goal_area", goal_area)
            py_trees.blackboard.Blackboard.set("go_to_area_behavior", "disabled")
            py_trees.blackboard.Blackboard.set("chatgpt/function_call","")
            return py_trees.common.Status.SUCCESS
        except Exception as e:
            self.logger.error("Exception:", str(e))
        return py_trees.common.Status.FAILURE  

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
    
    def go_to_area(self,goal_area:str,go_through_area:str):
        poses = []
        try:
            if go_through_area in self.regions:
                pose = PoseStamped()
                pose.header.frame_id = 'map'
                pose.pose.position.x = self.regions[go_through_area][0][0]
                pose.pose.position.y = self.regions[go_through_area][0][1]
                pose.pose.orientation.x = 0.0
                pose.pose.orientation.y = 0.0
                pose.pose.orientation.w = self.regions[go_through_area][1][0]
                pose.pose.orientation.z = self.regions[go_through_area][1][1]

                poses.append(pose)
           
            # Add the goal pose last
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.pose.position.x = self.regions[goal_area][0][0]
            goal_pose.pose.position.y = self.regions[goal_area][0][1]
            goal_pose.pose.orientation.x = 0.0
            goal_pose.pose.orientation.y = 0.0
            goal_pose.pose.orientation.w = self.regions[goal_area][1][0]
            goal_pose.pose.orientation.z = self.regions[goal_area][1][1]

            poses.append(goal_pose)
            self.logger.info("Poses: %s", poses)
            py_trees.blackboard.Blackboard.set("robot_control/goal_poses", poses)

        except Exception as e:
            self.logger.error(str(e))
        


    def load_regions_from_yaml(self,file_path):
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

            map_regions = {}
            for region, info in data.items():
                centroid = [info['centroid']['x'], info['centroid']['y']]
                orientation = [info['orientation']['w'], info['orientation']['z']]
                map_regions[region] = centroid,orientation
        except Exception as e:
            self.logger.error(str(e))

        return map_regions

