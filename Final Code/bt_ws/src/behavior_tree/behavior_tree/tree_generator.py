#!/usr/bin/env python3
import sys
import rclpy
import logging
import operator
import argparse
import py_trees
import threading
import py_trees.console as console
import bdai_ros2_wrappers.process as ros_process

from typing import Optional
from rclpy.node import Node
from datetime import datetime
from std_msgs.msg import String
from .config import settings as s
from .behaviors.hri_behaviors.ChatGPT import ChatGPT
from .behaviors.hri_behaviors.Microphone import Microphone
from .behaviors.hri_behaviors.SpeechToText import SpeechToText
from .behaviors.hri_behaviors.StopDetection import StopwordDetection
from .behaviors.hri_behaviors.WakewordDetection import WakewordDetection
from .behaviors.hri_behaviors.SpeechSynthesizer import SpeechSynthesizer
from .behaviors.robot_control_behaviors.Navigation import Navigation
from .behaviors.robot_control_behaviors.SpotControl import RobotControl
from .behaviors.robot_control_behaviors.ObjectDetection import ObjectDetection
from .behaviors.command_center.BehaviorHandler import BehaviorHandler
from .behaviors.command_center.GoToAreaBehavior import GoToArea
from .behaviors.command_center.LocateObjectBehavior import LocateObject
from .behaviors.command_center.TalkBehavior import TalkToOperator
from .behaviors.system_check.RobotState import RobotState
from .behaviors.system_check.Bootup import Bootup



####################################################################
# Visualization Variables
FONT_SIZE = 15
level = 1
start_y = 20 
running = True
nodes_to_ignore = ["Keyword Guard","Keyword Guard Inverter", "Spot Control Guard", "Spot Control Guard Inverter", "Listener Guard", "Listener Guard Inverter"]
####################################################################

def create_root(logger: logging.Logger, robot_name: Optional[str] = None, node: Optional[Node] = None) -> py_trees.behaviour.Behaviour: # 
    """
    Setup of Spot Behavior Tree. Returns root of tree.
    """
    py_trees.blackboard.Blackboard.set("input_text_command", "")
    py_trees.blackboard.Blackboard.set("chatgpt/msg", "")
    py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
    py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", [])  
    py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
    py_trees.blackboard.Blackboard.set("spot_sleeping", True)
    py_trees.blackboard.Blackboard.set("spot_stop", False)
    py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
    py_trees.blackboard.Blackboard.set("robot_control/detect_object", None)
    py_trees.blackboard.Blackboard.set("first_run", True)          ##########
    py_trees.blackboard.Blackboard.set("object_found", False)
    py_trees.blackboard.Blackboard.set("current_location", "home")

    root = py_trees.composites.Parallel(name="Spot", policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False))
    root_repeater = py_trees.decorators.Repeat(name="Root", child=root, num_success=-1)
    logger = createLogger()
    #################### Tasks that need to be run parallel ####################
    listen = Microphone(name="Microphone", logger=logger)
    
    cancel_task = StopwordDetection(name="Stopword Detection", chunk=s.kw_chunk, logger=logger)
    spot_sequence = py_trees.composites.Sequence(name="Behavior Sequence", memory=True)
    spot_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=SpotAllowedToMove, blackboard_keys={"spot_stop"}, child=spot_sequence)
    spot_guard_inverter = py_trees.decorators.FailureIsSuccess("FailureIsSuccess", spot_guard)

    system_check = py_trees.composites.Sequence(name="System Check", memory=True)

    #################### system_check Subtree ####################
    robot_check = RobotState(name="Robot State",robot_name=robot_name, node=node, logger=logger)
    #system_failure = SpeechSynthesizer(name="Speech Synthesization", topic="system_check", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    boot_up = Bootup(name="Robot boot up",robot_name=robot_name, node=node, logger=logger)
    oneshot=py_trees.decorators.OneShot(name="Oneshot Bootup",child=boot_up,policy=py_trees.common.OneShotPolicy.ON_SUCCESSFUL_COMPLETION)
    # #################### HRI Subtree ####################
    hri_tasks = py_trees.composites.Sequence(name="User Interaction", memory=True)
    

    sit_down_robot = RobotControl(name="Spot Control - Go To Sleep",robot_name=robot_name, node=node, task="sit", logger=logger)
    detect_keyword = WakewordDetection(name="Wakeword Detection", chunk=s.kw_chunk, logger=logger) #, sample_rate=s.mic_sample_rate, chunk=s.kw_chunk
    initialize_robot = RobotControl(name="Spot Control - Wake Up", robot_name=robot_name, node=node, task="stand", logger=logger)
    # Speaking Subtree
    say_hey = SpeechSynthesizer(name="Speech Synthesizer",topic="text_to_speak/startup", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    talk_movement_hey = RobotControl(name="Spot Control - Talk", robot_name=robot_name, node=node, task="talk", logger=logger)
    say_hey_subtree = py_trees.composites.Parallel("Speak: Hey", policy=py_trees.common.ParallelPolicy.SuccessOnSelected(children=[say_hey],synchronise=False), children=[say_hey, talk_movement_hey])
    
    listen_for_command = SpeechToText(name="Speech to Text - Transcription",  
                                               phrase_timeout=s.phrase_timeout,
                                               input_timeout=s.input_timeout, 
                                               whisper_version=s.whisper_version,
                                               model=s.model,
                                               logger=logger,
                                               save_data=s.save_data)    
    listener_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=IsSpotListening, blackboard_keys={"spot_waiting_for_command"}, child=listen_for_command)
    listener_guard_inverter = py_trees.decorators.FailureIsSuccess("FailureIsSuccess", listener_guard)
 
    
    wake_up_subtree = py_trees.composites.Sequence(name="Wake Up Subtree", memory=True, children=[sit_down_robot, detect_keyword, initialize_robot, say_hey_subtree]) #, keyword_guard_inverter, initialize_robot, say_hey
    wake_up_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=IsSpotSleeping, blackboard_keys={"spot_sleeping"}, child=wake_up_subtree)
    wake_up_guard_inverter = py_trees.decorators.FailureIsSuccess("FailureIsSuccess", wake_up_guard)



    chatGPT = ChatGPT(name="GPT", logger=logger)
    chatGPT_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=ChatGPTActive, blackboard_keys={"ChatGPT_active"}, child=chatGPT)
    chatGPT_guard_inverter = py_trees.decorators.FailureIsSuccess("FailureIsSuccess", chatGPT_guard)


    #################### Spot Behaviors Subtree ####################
    command_center_tasks = py_trees.composites.Sequence(name="Decision Center", memory=True)
    command_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=IsSpotActive, blackboard_keys={"spot_sleeping"}, child=command_center_tasks)
    command_guard_inverter = py_trees.decorators.FailureIsSuccess("FailureIsSuccess", command_guard)

    
    behavior_handler = BehaviorHandler(name="Behavior Handler", logger=logger)
    
    # Add behavior subtrees
    talk_to_operator_behavior = py_trees.composites.Sequence(name="Talk_To_Operator",  memory= True)
    go_to_area_behavior = py_trees.composites.Sequence(name="Go_To_Area", memory= True)
    locate_object_behavior = py_trees.composites.Sequence(name="Locate_Object",  memory=True)
    back_to_sleep = py_trees.composites.Sequence(name="Back_To_Sleep" ,  memory= True)
    
    py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "disabled")
    py_trees.blackboard.Blackboard.set("go_to_area_behavior", "disabled")
    py_trees.blackboard.Blackboard.set("locate_object_behavior", "disabled")
    py_trees.blackboard.Blackboard.set("go_back_to_sleep_behavior", "disabled")

    choose_behavior = py_trees.idioms.either_or(
        name="Behavior Chooser",
        conditions=[
            py_trees.common.ComparisonExpression("talk_to_operator_behavior", "enabled", operator.eq),
            py_trees.common.ComparisonExpression("go_to_area_behavior", "enabled", operator.eq),
            py_trees.common.ComparisonExpression("locate_object_behavior", "enabled", operator.eq),
        ],
        subtrees=[talk_to_operator_behavior, go_to_area_behavior, locate_object_behavior],
        namespace="either_or"
    )

    #################### Set up individual behavior subtrees ####################
    # Talk to operator
    talk_setup = TalkToOperator(name="Talk Behavior Setup", logger=logger)
    talk = SpeechSynthesizer(name="Speech Synthesizer", topic="text_to_speak/talk", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    talk_movement = RobotControl(name="Spot Control - Talk", robot_name=robot_name, node=node, task="talk", logger=logger)
    talk_subtree = py_trees.composites.Parallel("Talk to Operator", policy= py_trees.common.ParallelPolicy.SuccessOnSelected(children=[talk],synchronise=False), children=[talk,talk_movement])
    
    # Go to pose
    go_to_area_setup = GoToArea(name="Go-To-Area Behavior Setup", logger=logger)
    go_to_area_say_ready = SpeechSynthesizer(name="Speech Synthesizer", topic="text_to_speak/go_to_area", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    navigate = Navigation(name = "Navigator", logger=logger)

    # Locate object
    locate_object_setup = LocateObject(name="Locate-Object Behavior Setup", logger=logger)
    locate_object_say_ready = SpeechSynthesizer(name="Speech Synthesizer", topic="text_to_speak/locate_object", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    locate = py_trees.composites.Parallel(name="Locating",  policy=py_trees.common.ParallelPolicy.SuccessOnOne())
    detect_object = ObjectDetection(name = "Object Detector", logger=logger)
    robot_look = RobotControl(name="Spot Control - Look", robot_name=robot_name, node=node, task="look_for_object", logger=logger)


    #################### Building tree ####################
    # Add parallel running tasks to spot_sequence
    root.add_children([system_check, listen, cancel_task, spot_guard_inverter ])

    # Add system check Subtree to root
    system_check.add_children([robot_check, oneshot]) #[robot_check,system_failure,oneshot]

    # Add HRI Subtree to root
    spot_sequence.add_child(hri_tasks)
    #hri_tasks.add_children([sit_down_guard_inverter, keyword_guard_inverter, initialize_robot, say_hey, listen_for_command])
    hri_tasks.add_children([wake_up_guard_inverter, listener_guard_inverter])
    # Add Command Center Subtree to spot_sequence
    spot_sequence.add_child(command_guard_inverter)
    command_center_tasks.add_children([chatGPT_guard_inverter, behavior_handler, choose_behavior]) 
    
    # Add individual subbehavior tasks 
    talk_to_operator_behavior.add_children([talk_setup, talk_subtree])
    go_to_area_behavior.add_children([go_to_area_setup, go_to_area_say_ready, navigate]) # robot sleep
    locate_object_behavior.add_children([locate_object_setup, locate_object_say_ready, locate])
    locate.add_children([detect_object, robot_look])

    logger.info("Behavior Tree Generated.")
    return root

def IsSpotSleeping(blackboard):
    return blackboard.spot_sleeping

def IsSpotActive(blackboard):
    if blackboard.spot_sleeping:
        return False
    return True

def SpotAllowedToMove(blackboard):
    if blackboard.spot_stop:
        return False
    return True


def IsSpotListening(blackboard):
    return blackboard.spot_waiting_for_command

def ChatGPTActive(blackboard):
    return blackboard.ChatGPT_active

# def visualization_thread(tree, publisher, logger):
#     global running
#     global level
#     behavior_tree_info = []

#     def publish_behavior_tree_info():
#         try: 
#             # Generate the behavior tree information
#             draw_behavior_tree(tree.root, 50)
#             # Format the behavior tree information as a string and publish it
#             draw_behavior_tree(tree.root, 50)
#             msg = String()
#             msg.data = "\n".join(behavior_tree_info)
#             publisher.publish(msg)
#         except Exception as e: 
#             logger.error(str(e))

#     def draw_behavior_tree(tree_node, x):
#         try:
#             global level
#             if tree_node.status == py_trees.common.Status.RUNNING:
#                 color = 'yellow'
#             elif tree_node.status == py_trees.common.Status.SUCCESS:
#                 color = 'green'
#             elif tree_node.status == py_trees.common.Status.FAILURE:
#                 color = 'red'
#             else: 
#                 color = 'white'
#             # Draw current node
#             y = start_y + FONT_SIZE * (level) * 1.5
#             # draw_text(tree_node.name, x, y, color)
#             behavior_tree_info.append(f"{tree_node.name},{x},{y},{color}")
#             level += 1
#             x += 50
#             for child in tree_node.children:
#                 draw_behavior_tree(child, x)
#         except Exception as e:
#             logger.error(str(e))

#     while running:
#         level = 1
#         publish_behavior_tree_info()
#         time.sleep(0.1)
      
def createLogger():
    logger = logging.getLogger("BehaviorTreeLog")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s')
    file_name = datetime.now().strftime("/home/nuc242/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/Audio_files/%Y-%m-%d-%H-%M-%S.log")
    filehandler = logging.FileHandler(file_name)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger

def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default=None)
    return parser

@ros_process.main(cli())
def main(args: argparse.Namespace):
    logger = createLogger()
    root = create_root(logger=logger, robot_name=args.robot, node=main.node)

    tree = py_trees.trees.BehaviourTree(
        root=root,
        unicode_tree_debug=True
    )

    try:
        tree.setup(timeout=15)
    except py_trees.exceptions.TimedOutError as e:
        console.logerror(console.red + "failed to set up the tree, aborting [{}]".format(str(e)) + console.reset)
        tree.shutdown()
        rclpy.try_shutdown()
        sys.exit(1)
    tree_pub = tree.node.create_publisher(String, "/behavior_tree", 10)
    # vis_thread = threading.Thread(target=visualization_thread, args=(tree,tree_pub,logger,))
    # vis_thread.start()

    tree.tick_tock(period_ms=100.0)

    try:
        rclpy.spin(tree.node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        global running
        running = False
        # vis_thread.join()
        tree.shutdown()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()