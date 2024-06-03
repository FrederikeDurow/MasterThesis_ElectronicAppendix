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
            kw_path0 = os.path.join(current_path, "src/multiple_functions/multiple_functions/config/keyworddetection/Spot-cancel-task_en_linux_v3_0_0.ppn")
            kw_path1 = os.path.join(current_path, "src/multiple_functions/multiple_functions/config/keyworddetection/Spot-Stop_en_linux_v3_0_0.ppn")
            self.porcupine = pvporcupine.create(
                    access_key="nPEGLfpx3i0HGziIbgRG3L3CLNIhXrBNkhmDaRekehwTDFfqRnmfIA==", # Frederike
                    keyword_paths = [kw_path0, kw_path1]
                )
            
            # Create subscriber to get microphone input
            self.voiceComSubscriber = self.node.create_subscription(AudioData, '/audio/channel0', self.callback, 10)
        except Exception as e: 
            self.logger.error(str(e))
        
    def initialise(self) -> None:
        self.keyword_detected = False
        self.feedback_message = "Waiting for keyword"

    def update(self) -> Status:
        try: 
            if self.keyword_detected == True: 
                self.logger.info("Keyword detected!")
                self.feedback_message = "Keyword detected: Spot Cancel Task!"
                # py_trees.blackboard.Blackboard.set("text_to_speak/startup","Hey, I'm Spot, how may i help you?")
                py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                py_trees.blackboard.Blackboard.set("navigation/cancel_task", True)
                return py_trees.common.Status.SUCCESS
            else:
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
                    self.keyword_detected = True
        except Exception as e: 
            self.logger.error(str(e))
            

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)