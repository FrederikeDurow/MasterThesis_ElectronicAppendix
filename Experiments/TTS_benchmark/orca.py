import pvorca
from io import BytesIO
import pyaudio
import wave
import struct

orca = pvorca.create(access_key="px6MFm1HSRLrFsNmBzvRT4GAGd30CPaNdV/czEsf9C+eZHpr7O5NOQ==",model_path="/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/orca_params_male.pv")



orca.synthesize_to_file(text="Hey I'm Spot. How may i help you?", output_path="/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/Generated_audio/orca2_audio.wav")