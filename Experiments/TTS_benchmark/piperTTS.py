from dimits import Dimits

# Initialize Dimits with the desired voice model
dt = Dimits("en_US-ryan-high")

# Convert text to audio and play it using the aplay engine
dt.text_2_speech("Hello, I'm Spot, How may i help you?. I'm able to look for a banana go to location like a kitchen. Is there any thing you need?", engine="aplay")