import torch
from TTS.api import TTS

print(TTS().list_models())

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/en/ek1/tacotron2").to(device)

tts.tts_to_file(text="Hey I'm Spot. How may i help you?", file_path="/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/Generated_audio/Generated_audio.wav")



#tts_models/en/ljspeech/glow-tts
#tts_models/en/ljspeech/tacotron2-DCA
#tts_models/en/ljspeech/speedy-speech-wn
#tts_models/en/sam/tacotron-DDC
#tts_models/en/vctk/sc-glow-tts 

