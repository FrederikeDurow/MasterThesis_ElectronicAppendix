from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine

engine = SystemEngine() # replace with your TTS engine
stream = TextToAudioStream(engine)
stream.feed("Hey I'm Spot. How may i help you?")
stream.play()

#NLTK Sentence Tokenizer: Uses the Natural Language Toolkit's sentence tokenizer for precise and efficient sentence segmentation.