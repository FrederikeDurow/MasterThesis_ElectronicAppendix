#!/usr/bin/env python3
import sys
import time
import rclpy
import logging
import operator
import argparse
import py_trees
import threading
import py_trees_ros.trees
import py_trees.console as console

from typing import Optional
from rclpy.node import Node
from datetime import datetime
from .config import settings as s
from .behaviors.input_behaviors.Microphone import Microphone
from .behaviors.input_behaviors.SpeechToText import SpeechToText
from .behaviors.input_behaviors.StopDetection import StopwordDetection
from .behaviors.input_behaviors.WakewordDetection import WakewordDetection
from .behaviors.input_behaviors.SpeechSynthesizer import SpeechSynthesizer
from .behaviors.behavior_handling.ChatGPT import ChatGPT
from .behaviors.behavior_handling.BehaviorHandler import BehaviorHandler
from .behaviors.robot_behaviors.TalkBehaviorSetup import TalkToOperator
from .behaviors.robot_behaviors.PlaceProbesBehavior import PlaceProbes
from .behaviors.robot_behaviors.PlaceProbesSetup import PlaceProbesSetup



####################################################################
# Visualization Variables
FONT_SIZE = 15
level = 1
start_y = 20 
running = True
nodes_to_ignore = ["Keyword Guard","Keyword Guard Inverter", "Spot Control Guard", "Spot Control Guard Inverter", "Listener Guard", "Listener Guard Inverter"]
####################################################################

def create_root() -> py_trees.behaviour.Behaviour: # 
    """
    Setup of Spot Behavior Tree. Returns root of tree.
    """
    start_phrase = "Hey, how can I help you?"

    logger = createLogger()
    py_trees.blackboard.Blackboard.set("hri/text_command", "")
    py_trees.blackboard.Blackboard.set("chatgpt/msg", "")
    py_trees.blackboard.Blackboard.set("spot_sleeping", True)
    py_trees.blackboard.Blackboard.set("robot_stop", False)
    py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
    py_trees.blackboard.Blackboard.set("spot/movement_done", True)
    py_trees.blackboard.Blackboard.set("spot/stop_moving", False)
    py_trees.blackboard.Blackboard.set("robot_control/detect_object", None)
    py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
    py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", []) ########## 
    py_trees.blackboard.Blackboard.set("first_run", True)          ##########
    py_trees.blackboard.Blackboard.set("chatgpt/reset", True)      ########## Burde ikke være nødvendig, da WakeWord sætter den
    py_trees.blackboard.Blackboard.set("STT_flag", True)
    py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg",False)
    py_trees.blackboard.Blackboard.set("StopKeyword", False)
    py_trees.blackboard.Blackboard.set("object_found", False)
    py_trees.blackboard.Blackboard.set("current_location", "home")


    root = py_trees.composites.Parallel(name="Spot", policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False))
    root_repeater = py_trees.decorators.Repeat(name="Root", child=root, num_success=-1)

    #################### Tasks that need to be run parallel ####################
    listen = Microphone(name="Microphone", logger=logger)
    
    cancel_task = StopwordDetection(name="Stopword Detection", chunk=s.kw_chunk, logger=logger)
    main_sequence = py_trees.composites.Sequence(name="Main Sequence", memory=True)
    main_guard = py_trees.decorators.EternalGuard(name= "Main Guard", condition=SpotAllowedToMove, blackboard_keys={"robot_stop"}, child=main_sequence)
    main_guard_inverter = py_trees.decorators.FailureIsSuccess("Main Guard Inverter", main_guard)

   
    ##################### HRI Subtree ####################
    input_sequence = py_trees.composites.Sequence(name="Human-Robot Interaction", memory=True)
    

    detect_keyword = WakewordDetection(name="Wakeword Detection", chunk=s.kw_chunk, start_phrase=start_phrase, logger=logger) #, sample_rate=s.mic_sample_rate, chunk=s.kw_chunk
    say_hey = SpeechSynthesizer(name="Speech Synthesization",topic="text_to_speak/startup", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    listen_for_command = SpeechToText(name="Speech to Text - Transcription",  
                                               phrase_timeout=s.phrase_timeout,
                                               input_timeout=s.input_timeout, 
                                               whisper_version=s.whisper_version,
                                               model=s.model,
                                               logger=logger,
                                               save_data=s.save_data)    
    listener_guard = py_trees.decorators.EternalGuard(name= "Listener Guard", condition=IsSpotListening, blackboard_keys={"spot_waiting_for_command"}, child=listen_for_command)
    listener_guard_inverter = py_trees.decorators.FailureIsSuccess("Listener Guard Inverter", listener_guard)
 
    
    wake_up_subtree = py_trees.composites.Sequence(name="Wake Up Subtree", memory=True, children=[detect_keyword, say_hey]) 
    wake_up_guard = py_trees.decorators.EternalGuard(name= "Wake Up Guard", condition=IsSpotSleeping, blackboard_keys={"spot_sleeping"}, child=wake_up_subtree)
    wake_up_guard_inverter = py_trees.decorators.FailureIsSuccess("Wake Up Guard Inverter", wake_up_guard)



    chatGPT = ChatGPT(name="ChatGPT", logger=logger)
    chatGPT_guard = py_trees.decorators.EternalGuard(name= "Wake Up Guard", condition=ChatGPTActive, blackboard_keys={"ChatGPT_active"}, child=chatGPT)
    chatGPT_guard_inverter = py_trees.decorators.FailureIsSuccess("Wake Up Guard Inverter", chatGPT_guard)


    #################### Spot Behaviors Subtree ####################
    execution_sequence = py_trees.composites.Sequence(name="Command Center", memory=True)
    execution_guard = py_trees.decorators.EternalGuard(name= "Guard", condition=IsSpotActive, blackboard_keys={"spot_sleeping"}, child=execution_sequence)
    execution_guard_inverter = py_trees.decorators.FailureIsSuccess("Inverter", execution_guard)

    
    behavior_handler = BehaviorHandler(name="Behavior Handler", logger=logger)
    
    #################### Set up individual behavior subtrees ####################
    # Talk to operator
    talk_to_operator_behavior = py_trees.composites.Sequence(name="Talk_To_Operator",  memory= True)
    talk_setup = TalkToOperator(name="Talk Behavior Setup", logger=logger)
    talk = SpeechSynthesizer(name="Speech_Synthesizer", topic="text_to_speak/talk", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    talk_to_operator_behavior.add_children([talk_setup, talk])
    py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "disabled")

    # place_probes
    place_probes_behavior = py_trees.composites.Sequence(name="place_probes_behavior",  memory= True)
    place_probes_setup = PlaceProbesSetup(name="place_probes_setup", logger=logger)
    place_probes_talk = SpeechSynthesizer(name="speech_synthesizer", topic="text_to_speak/place_probes", voice=s.voice, language=s.language, volume=s.speech_volume, logger=logger)
    place_probes = PlaceProbes(name="place_probes", logger=logger)
    place_probes_behavior.add_children([place_probes_setup, place_probes_talk, place_probes])
    py_trees.blackboard.Blackboard.set("place_probes_behavior", "disabled")

    # ADD NEW BEHAVIORS HERE


    choose_behavior = py_trees.idioms.either_or(
        name="Behavior Chooser",
        conditions=[
            py_trees.common.ComparisonExpression("talk_to_operator_behavior", "enabled", operator.eq),
            py_trees.common.ComparisonExpression("place_probes_behavior", "enabled", operator.eq),
            # ADD NEW BEHAVIORS HERE
        ],
        subtrees=[talk_to_operator_behavior, place_probes_behavior], # ADD NEW BEHAVIORS HERE
        namespace="either_or"
    )

    #################### Building tree ####################
    # Add parallel running tasks to spot_sequence
    root.add_children([listen, cancel_task, main_guard_inverter])

    # Add HRI Subtree to root
    main_sequence.add_children([input_sequence, execution_guard_inverter])
    input_sequence.add_children([wake_up_guard_inverter, listener_guard_inverter])
    execution_sequence.add_children([chatGPT_guard_inverter, behavior_handler, choose_behavior]) 


   

    logger.info("Behavior Tree Generated.")
    return root

def IsSpotSleeping(blackboard):
    return blackboard.spot_sleeping

def IsSpotActive(blackboard):
    if blackboard.spot_sleeping:
        return False
    return True

def SpotAllowedToMove(blackboard):
    if blackboard.robot_stop:
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
    file_name = datetime.now().strftime("./behaviortree.log")
    filehandler = logging.FileHandler(file_name)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger

# def cli() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--robot", type=str, default=None)
#     return parser

# @ros_process.main(cli())
# def main(args: argparse.Namespace):
def main():
    # logger = createLogger()
    # root = create_root(logger=logger, robot_name=args.robot, node=main.node)
    rclpy.init(args=None)
    root = create_root()

    tree = py_trees_ros.trees.BehaviourTree(
        root=root,
        unicode_tree_debug=True
    )

    try:
        tree.setup(timeout=15)
    except py_trees_ros.exceptions.TimedOutError as e:
        console.logerror(console.red + "failed to set up the tree, aborting [{}]".format(str(e)) + console.reset)
        tree.shutdown()
        rclpy.try_shutdown()
        sys.exit(1)
    #tree_pub = tree.node.create_publisher(String, "/behavior_tree", 10)
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