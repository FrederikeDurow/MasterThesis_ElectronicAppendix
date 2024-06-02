#!/usr/bin/env python3

import logging
import py_trees
import numpy as np
import rclpy
import sounddevice as sd
import wave
from rclpy.node import Node
from py_trees.common import Status
from audio_common_msgs.msg import AudioData

class Microphone(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
        self.node = None
        self.stream = None
        self.audio_buffer = np.array([], dtype=np.int16)
        self.chunk_size = 1024  # Adjust chunk size as necessary
        self.sample_rate = 16000  # Common sample rate for audio

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = f"Didn't find 'node' in setup's kwargs [{self.qualified_name}]"
            raise KeyError(error_message) from e

        try:
            self._pub_audio = self.node.create_publisher(AudioData, 'audio/channel0', 10)
            self.stream = sd.InputStream(callback=self.audio_callback, channels=1, dtype='int16', samplerate=self.sample_rate)
            self.stream.start()
            self.logger.info("Microphone setup completed and audio stream started")
        except Exception as e:
            self.logger.error(e)

    def audio_callback(self, indata, frames, time, status):
        if status:
            self.logger.error(f"Audio callback status: {status}")
        
        self.audio_buffer = np.concatenate((self.audio_buffer, indata[:, 0]))

        while len(self.audio_buffer) >= self.chunk_size:
            audio_chunk = self.audio_buffer[:self.chunk_size]
            self.audio_buffer = self.audio_buffer[self.chunk_size:]
            self.on_audio(audio_chunk)

          
    def on_audio(self, data):
        audio_data_msg = AudioData(data=data.tobytes())
        self._pub_audio.publish(audio_data_msg)
   

    def initialise(self) -> None:
        pass

    def update(self) -> Status:
        try:
            return Status.RUNNING
        except Exception as e:
            self.logger.error(str(e))
            return Status.FAILURE

    def terminate(self, new_status: Status) -> None:
        self.logger.info(f"Microphone behaviour terminated with status {new_status}")
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
