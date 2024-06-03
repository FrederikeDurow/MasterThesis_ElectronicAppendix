import wave
import pyaudio
import py_trees
import logging
from typing import Any
from io import BytesIO
from py_trees.common import Status
from mimic3_tts import Mimic3Settings, Mimic3TextToSpeechSystem

class SpeechSynthesizer():
    def __init__(self, model :str):
        super().__init__()
        self.topic_name = model
        
        if model == "Mimic3":
            self.settings = Mimic3Settings(voice="en_US/cmu-arctic_low",  # info here
                voices_directories=None, #Directories to search for voices (<lang>/<voice>)
                speaker=8, # Default speaker name or id
                language="en_US",  # Set the language (if not using default)
                volume=100,  # Set the volume (0-100)
                rate=0.8,  # Set the speaking rate (adjust as needed)pi
                providers="CPUExecutionProvider",   # Other options: 'AzureExecutionProvider', 'CUDAExecutionProvider'
                no_download=True )# download voices automatically)# download voices automatically)
            # Create an instance of the Mimic3TextToSpeechSystem
            self.tts = Mimic3TextToSpeechSystem(self.settings)

        elif model == "Coqui":
            pass
    
    def update(self):
        # Read mtext message, generate speech from it
        try: 
            text_to_speak = py_trees.blackboard.Blackboard.get(self.topic_name)
            audio_bytes=self.tts.text_to_wav(text_to_speak)
            py_trees.blackboard.Blackboard.set(self.topic_name,"")

            temp_audio_file = BytesIO(audio_bytes)
            p = pyaudio.PyAudio()
            wf = wave.open(temp_audio_file, 'rb')
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            chunk = 1024
            data = wf.readframes(chunk)
            while data:
                stream.write(data)
                data = wf.readframes(chunk)

            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except Exception as e: 
            print(e)

def main():
    pass

if __name__ == "__main__":
    main()