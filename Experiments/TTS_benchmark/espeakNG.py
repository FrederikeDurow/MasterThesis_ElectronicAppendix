import subprocess

def synthesize_to_wav(text, filename):
    command = ['espeak', text, '--stdout']
    with open(filename, 'wb') as f:
        subprocess.run(command, stdout=f)

text = "Hello, this is a test of eSpeak NG."
synthesize_to_wav(text, 'output.wav')