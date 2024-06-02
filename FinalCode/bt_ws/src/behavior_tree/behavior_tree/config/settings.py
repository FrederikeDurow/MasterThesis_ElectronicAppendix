### Microphone Settings 
energy_threshold = 1000
record_timeout = 2
phrase_timeout = 1.3 # How many seconds of silence before the a sentence is considered done
command_timeout = 3 # How many seconds of silence before the command is considered done
input_timeout = 5 # How many seconds of silence before not waiting for command anymore

### Keyword Detection Settings
kw_chunk = 512  # Number of frames per buffer

## Speech Synthesizer Settings
voice="en_US/cmu-arctic_low",  # info here
voices_directories=None, #Directories to search for voices (<lang>/<voice>)
language="en_US",  # Set the language (if not using default)
speech_volume=100,  # Set the volume (0-100)
speech_rate=0.8,  # Set the speaking rate (adjust as needed)pi
speech_provider="CPUExecutionProvider",   # Other options: 'AzureExecutionProvider', 'CUDAExecutionProvider'
speech_no_download=True # download voices automatically

## Respeaker settings
RESPEAKER_PARAMETERS = {
    'CNIONOFF':0,            #'Comfort Noise Insertion.', '0 = OFF', '1 = ON'
    'AGCONOFF':1,            #'Automatic Gain Control. ', '0 = OFF ', '1 = ON'
    'AGCMAXGAIN':10,      #'Maximum AGC gain factor. ', 10dB = 3.162, 12dB = 3.981, 15dB = 7.079, 20dB = 10
    'AGCDESIREDLEVEL':0.005, #'Target power level of the output signal. ', -23dBov = 0.005,
    'AGCTIME':0.2,           #'Ramps-up / down time-constant in seconds.'
    
    # Static Noise reduction
    'GAMMA_NS':2.0,          #'Over-subtraction factor of stationary noise. min .. max attenuation
    'MIN_NS':0.15,           #'Gain-floor for stationary noise suppression.', default: -16dB = 20log10(0.15))'    
    
    # Dynamic Noise reduction
    'GAMMA_NN':1.1000,       #'Over-subtraction factor of non- stationary noise. min .. max attenuation'),
    'MIN_NN':0.3,            #'Gain-floor for non-stationary noise suppression.', (default: -10dB = 20log10(0.3))'),

    # VAD Parameters
    'GAMMA_NS_SR':1.0,       #'Over-subtraction factor of stationary noise for ASR. ', '(default: 1.0)'),
    'GAMMA_NN_SR':1.1,       #'Over-subtraction factor of non-stationary noise for ASR. ',(default: 1.1)'),
    'MIN_NS_SR':0.15,        #'Gain-floor for stationary noise suppression for ASR.', '(default: -16dB = 20log10(0.15))'),
    'MIN_NN_SR':0.3,         #'Gain-floor for non-stationary noise suppression for ASR.', '(default: -10dB = 20log10(0.3))'),
    'GAMMAVAD_SR':1.5,       #'Set the threshold for voice activity detection.', '(default: 3.5dB 20log10(1.5))'),
}

## Save data
save_data = True
model = "base.en"
whisper_version = "CT2"     #Ori = Original version, CT2 = Ctranslate version, JAX = Whisper_JAX