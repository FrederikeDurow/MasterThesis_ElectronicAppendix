import wave
import time
import pyaudio
import py_trees
import logging
import threading
from threading import Event
from typing import Any
from io import BytesIO
from py_trees.common import Status
from mimic3_tts import Mimic3Settings, Mimic3TextToSpeechSystem


class SpeechSynthesizer(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, topic: str, voice: str, language: str, volume: int, logger: logging.Logger):
        super().__init__(name=name)
        self.topic_name = topic
        self.voice = voice
        self.language = language
        self.volume = volume
        self.logger = logger

    def setup(self, **kwargs: Any) -> None:
        try:
            self.node = kwargs['node']
            self.speak_start = True
            self.event = Event()
        except Exception as e: 
            self.logger.error(str(e))

    def initialise(self) -> None:
        try:
            self.logger.info("SpeechSynthesizer")
            self.settings = Mimic3Settings(voice="en_US/cmu-arctic_low",  # info here
                voices_directories=None, #Directories to search for voices (<lang>/<voice>)
                speaker=8, # Default speaker name or id, only important for multi-speaker models 
                language="en_US",  # Set the language (if not using default)
                volume=100,  # Set the volume (0-100)
                rate=0.8,  # Set the speaking rate (adjust as needed)pi
                providers="CPUExecutionProvider",   # Other options: 'AzureExecutionProvider', 'CUDAExecutionProvider'
                no_download=True )# download voices automatically)# download voices automatically)
            # Create an instance of the Mimic3TextToSpeechSystem
            self.tts = Mimic3TextToSpeechSystem(self.settings)
            self.speak_start = True
            self.speaker_thread = None
            self.event.clear()
            
            py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW") 
            
        except Exception as e: 
            self.logger.error(str(e))
    
    def update(self) -> Status:
        # Read mtext message, generate speech from it
        try:
            if self.speak_start:
                # py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW") 
                text_to_speak = py_trees.blackboard.Blackboard.get(self.topic_name)
                py_trees.blackboard.Blackboard.set(self.topic_name,"")
                audio_bytes=self.tts.text_to_wav(text_to_speak)
                temp_audio_file = BytesIO(audio_bytes)
                p = pyaudio.PyAudio()
                wf = wave.open(temp_audio_file, 'rb')
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
                self.speaker_thread = threading.Thread(target=speaker_function, args=(self.event,stream,wf,p,self.logger,))
                self.speaker_thread.start()
                self.speak_start = False
            
            elif not self.speaker_thread.is_alive():
                return py_trees.common.Status.SUCCESS
    
            return py_trees.common.Status.RUNNING

        except Exception as e: 
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE
        
    
    def terminate(self, new_status: Status) -> None:
        self.event.set()
        # if self.speaker_thread.is_alive():
        #     self.speaker_thread.join()
        return super().terminate(new_status)
    
        
def speaker_function(event: Event, stream ,wf,p, logger): 
    try: 
        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            if event.is_set():
                break
            else:
                stream.write(data)
                data = wf.readframes(chunk)
            

        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e: 
        logger.error(str(e))