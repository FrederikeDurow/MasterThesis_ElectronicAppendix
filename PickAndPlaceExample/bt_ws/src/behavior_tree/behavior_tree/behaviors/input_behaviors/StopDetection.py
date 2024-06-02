import pvporcupine
from py_trees.common import Status
import numpy as np
import os
import py_trees
from audio_common_msgs.msg import AudioData 
import os
import logging

class StopwordDetection(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, chunk: int, logger: logging.Logger):
        super().__init__(name=name)
        self.chunk_size = chunk 
        self.logger = logger

        
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e 
        try: 
        # Initialize Porcupine with the desired keyword file
            current_path = os.getcwd()
            keyword_directory = os.path.join(current_path, "src/behavior_tree/behavior_tree/config/keyworddetection/StopWords")
            keyword_files = os.listdir(keyword_directory)
            keyword_paths = [os.path.join(keyword_directory, file) for file in keyword_files]

            self.porcupine = pvporcupine.create(
                access_key="nPEGLfpx3i0HGziIbgRG3L3CLNIhXrBNkhmDaRekehwTDFfqRnmfIA==", # Frederike
                keyword_paths=keyword_paths
            )
            
            # Create subscriber to get microphone input
            self.voiceComSubscriber = self.node.create_subscription(AudioData, '/audio/channel0', self.callback, 10)
        except Exception as e: 
            self.logger.error(str(e))
        
    def initialise(self) -> None:
        self.keyword_detected = False
        self.feedback_message = "Waiting for keyword"
        py_trees.blackboard.Blackboard.set("robot_stop", False)

    def update(self) -> Status:
        try: 
            if self.keyword_detected == True: 
                self.logger.info("Keyword detected!")
                py_trees.blackboard.Blackboard.set("robot_stop", True)
                py_trees.blackboard.Blackboard.set("STT_flag", True)
                py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
                py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                return py_trees.common.Status.SUCCESS
            return py_trees.common.Status.RUNNING         
        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE 

        
    def callback(self, msg):
        try: 
            pcm = np.frombuffer(msg.data, dtype=np.int16)
            for i in range(0, len(pcm), self.chunk_size):
                chunk = pcm[i:i+self.chunk_size]
                chunk = chunk.reshape((512, 1))

                keyword_index = self.porcupine.process(chunk.flatten())
                if keyword_index == 0 or keyword_index == 1:
                    self.logger.info("Keyword detected: %s", keyword_index)
                    self.keyword_detected = True
        except Exception as e: 
            self.logger.error(str(e))
            

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)