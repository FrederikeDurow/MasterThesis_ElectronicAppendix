import io
import os
import py_trees
import torch
import whisper
from queue import Queue
from datetime import datetime
from py_trees.common import Status
import speech_recognition as sr
from audio_common_msgs.msg import AudioData 
from std_msgs.msg import String
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import numpy as np
import logging
import numpy as np
from scipy.io.wavfile import write
import wave
import cProfile
import pstats
from .transcriber import WhisperModel
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp

class SpeechToText(py_trees.behaviour.Behaviour):

    def __init__(self, name: str, phrase_timeout: int, input_timeout: int, whisper_version: str, model: str, logger: logging.Logger, save_data: bool):
        super().__init__(name=name)
        try: 
            self.phrase_timeout=phrase_timeout 
            self.input_timeout=input_timeout
            self.logger = logger
            self.save_data = save_data
            hub_path = torch.hub.get_dir()
            model_path = os.path.join(hub_path, "snakers4_silero-vad_master")
            self.sal_model, _ = torch.hub.load(repo_or_dir=model_path,
                                model='silero_vad',
                                source='local',
                                force_reload=True)
            self.model = model
            self.whisper_version = whisper_version
            if self.whisper_version  == "Ori":
                self.audio_model = whisper.load_model(model)
            elif self.whisper_version  == "CT2":
                self.audio_model = WhisperModel(model_size_or_path=self.model, device="cpu", compute_type="int8")
            elif self.whisper_version  == "JAX":
                self.audio_model = FlaxWhisperPipline(checkpoint="openai/whisper-base.en",batch_size=1, dtype=jnp.bfloat16) #openai/whisper-tiny.en, openai/whisper-base.en, openai/whisper-small.en, openai/whisper-medium.en, 
            else:
                self.logger.error("Wrong whisper_version, please use Ori, CT2 or JAX")

        except Exception as e: 
            self.logger.error(str(e))

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.audioQueue = []
            self.subsriber = self.node.create_subscription(String, '/chatgpt/input', self.callback, 10)
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  

        
    def initialise(self) -> None:
        try: 
            # Create subscriber to get microphone input
            self.audioQueue = []
    
            self.time_last_input = None # The last time a recording was retreived from the queue.
            self.last_sample = bytes() # Current raw audio bytes.
            self.data_queue = Queue() # Thread safe Queue for passing data from the threaded recording callback.
            self.phrase_started = False
        
            # Load/Download model
            self.temp_file = NamedTemporaryFile().name
            #self.logger.info("Initialized = %s", self.temp_file)
            self.transcription =""

            self.phrase_complete = False
        
            # TimeStamps: 
            self.time_last_input = datetime.utcnow()
            self.start_time = datetime.utcnow()
            self.count=0

            # Process live audio data in chunks
            py_trees.blackboard.Blackboard.set("spot_sleeping", False)

        except Exception as e: 
            self.logger.error(str(e))

    def update(self) -> py_trees.common.Status:
        try:
            flag = py_trees.blackboard.Blackboard.get("STT_flag")
            if flag:                
                if len(self.transcription) != 0:
                    py_trees.blackboard.Blackboard.set("hri/text_command", self.transcription)
                    py_trees.blackboard.Blackboard.set("spot_waiting_for_command", False)
                    py_trees.blackboard.Blackboard.set("STT_flag", False)
                    return py_trees.common.Status.SUCCESS
                else:

                    return py_trees.common.Status.RUNNING
            else:
                return py_trees.common.Status.SUCCESS
        except Exception as e: 
            self.logger.error(str(e))
            py_trees.blackboard.Blackboard.set("spot_sleeping", True)
            
        return py_trees.common.Status.FAILURE
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
     

    def callback (self, msg)-> None:
        try:
            if msg:
                self.transcription = msg.data
        except Exception as e: 
            self.logger.error(str(e))

     
