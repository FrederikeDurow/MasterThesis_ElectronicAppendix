import io
import os
import torch
import whisper
import py_trees
import jax.numpy as jnp
import speech_recognition as sr
import numpy as np
import logging
import wave
import cProfile
import pstats

from queue import Queue
from datetime import datetime
from py_trees.common import Status
from audio_common_msgs.msg import AudioData 
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from .transcriber import WhisperModel
from whisper_jax import FlaxWhisperPipline
from rnnoise_wrapper import RNNoise

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
            self.denoiser = RNNoise()
            self.stt_running = True
            self.voiceComSubscriber = self.node.create_subscription(AudioData, '/audio/channel0', self.mic_callback, 10)
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  

        
    def initialise(self) -> None:
        try: 
            self.logger.info("SpeechToText")
            self.audioQueue = []
            self.stt_running = True
            self.time_last_input = None # The last time a recording was retreived from the queue.
            self.last_sample = bytes() # Current raw audio bytes.
            self.data_queue = Queue() # Thread safe Queue for passing data from the threaded recording callback.
            self.phrase_started = False
        
            # Load/Download model
            self.temp_file = NamedTemporaryFile().name
            self.transcription =""

            self.phrase_complete = False
        
            # TimeStamps: 
            self.time_last_input = datetime.utcnow()
            self.start_time = datetime.utcnow()
            self.count=0

            # Process live audio data in chunks

        except Exception as e: 
            self.logger.error(str(e))

    def update(self) -> py_trees.common.Status:
        try:
            py_trees.blackboard.Blackboard.set("LED_COLOR", "GREEN")   
            now = datetime.utcnow()
            if not self.audioQueue and self.phrase_started:
            # If enough time has passed between recordings, consider the phrase complete. Clear audio buffer
                    if (now - self.time_last_input) > timedelta(seconds=self.phrase_timeout):
                            try:
                                py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW") 
                                profiler = cProfile.Profile()
                                profiler.enable()
                                if self.whisper_version  == "Ori":
                                    result = self.audio_model.transcribe(self.temp_file, fp16=torch.cuda.is_available())
                                    self.transcription = result['text'].strip()
                                elif self.whisper_version  == "CT2":
                                    result,_= self.audio_model.transcribe(language="en",without_timestamps=True,audio=self.temp_file)
                                    if result: 
                                        self.transcription = result[0].text
                                    else:
                                        self.logger.info("WORKS")
                                        py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
                                        py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                                        self.stt_running = False
                                        return py_trees.common.Status.FAILURE
                                elif self.whisper_version  == "JAX":
                                    result = self.audio_model(self.temp_file,language="en",task="transcribe")
                                    self.transcription = result['text']
                      
                                profiler.disable()
                                stats = pstats.Stats(profiler).sort_stats('ncalls')
                                if len(self.transcription) == 0:
                                    py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                                    self.stt_running = False
                                    return py_trees.common.Status.FAILURE
                                py_trees.blackboard.Blackboard.set("input_text_command", self.transcription)
                                py_trees.blackboard.Blackboard.set("LED_COLOR","YELLOW")
                            except Exception as e: 
                                self.logger.error(e)
                            try:
                                if self.save_data:
                                
                                    save_folder = "src/behavior_tree/behavior_tree/Audio_files"  # Update with your desired folder path
                                    os.makedirs(save_folder, exist_ok=True)

                                    # Generate a unique filename, for example, using a timestamp
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    filename = f"audio_{timestamp}.wav"

                                    full_path = os.path.join(save_folder, filename)

                                    # Save transcription to a text file if needed
                                    transcription_filename = "transcription_log.txt"
                                    transcription_full_path = os.path.join(save_folder, transcription_filename)
                                    # Append the transcription and timestamp to the existing text file
                                    with open(transcription_full_path, 'a') as transcription_file:
                                        transcription_file.write(f"{timestamp}: {self.transcription} | {stats.get_stats_profile().total_tt:.4f}\n")
                                    
                                    # Save the audio data as a WAV file using the wave module
                                    with open(self.temp_file, 'rb') as temp_file, wave.open(full_path, 'wb') as wf:
                                    #with wave.open(full_path, 'wb') as wf:

                                        wf.setnchannels(1)  # Assuming mono audio, change to 2 for stereo
                                        wf.setsampwidth(2)  # Adjust according to your sample width (2 bytes for 16-bit PCM)
                                        wf.setframerate(16000)  # Adjust according to your sample rate
                                        wf.writeframes(temp_file.read())
                                        wf.close()

                            except Exception as e:
                                self.logger.error(str(e))

                            self.last_sample = bytes()
                            self.audioQueue.clear()
                            os.remove(self.temp_file)
                            py_trees.blackboard.Blackboard.set("spot_waiting_for_command", False)
                            py_trees.blackboard.Blackboard.set("spot_sleeping", False)
                            self.stt_running = False
                            return py_trees.common.Status.SUCCESS
            
            elif self.phrase_started:
                try: 
                    for _ in range(len(self.audioQueue)):
                        self.time_last_input = now # Last time we received new audio data from the queue.
                        self.last_sample += self.audioQueue[0]
                        self.audioQueue.pop(0)

                    audio_data = sr.AudioData(self.last_sample, 16000, 2) # sample rate, sample width
                    
                    wav_data = io.BytesIO(audio_data.get_wav_data())    
                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data.read())
                except Exception as e: 
                    self.logger.error("EXCEPTION 1")
                    

            # Stop waiting for command after some time has passed
            elif (now - self.start_time) > timedelta(seconds=self.input_timeout):
                py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
                py_trees.blackboard.Blackboard.set("spot_sleeping", True)
                self.stt_running = False
                return py_trees.common.Status.FAILURE

            self.feedback_message = "Waiting for command"
            return py_trees.common.Status.RUNNING

        except Exception as e: 
            self.logger.error(str(e))
            py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
            py_trees.blackboard.Blackboard.set("spot_sleeping", True)
            self.stt_running = False
        return py_trees.common.Status.FAILURE
    
    # Provided by Alexander Veysov
    def int2float(self,sound):
        try:
            abs_max = np.abs(sound).max()
            sound = sound.astype('float32')
            if abs_max > 0:
                sound *= 1/32768
            sound = sound.squeeze()  # depends on the use case
        except Exception as e: 
            self.logger.error(str(e))
        return sound

    def mic_callback(self, msg: AudioData):
        try: 
            if self.stt_running is True:
                audio_int16 = np.frombuffer(msg.data, np.int16)
                audio_float32 = self.int2float(audio_int16)
                new_confidence = self.sal_model(torch.from_numpy(audio_float32), 16000).item()
                if new_confidence >= 0.65:
                    self.audioQueue.append(msg.data)
                    self.phrase_started = True
            else: 
                self.audioQueue.append(msg.data)
                if len(self.audioQueue) > 10: 
                    self.audioQueue.pop(0)


        except Exception as e: 
            self.logger.error(str(e))

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
     



     


