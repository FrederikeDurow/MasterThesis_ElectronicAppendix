import os
import csv
from jiwer import wer  # Install with `pip install jiwer`
import speech_recognition as sr  # Install with `pip install SpeechRecognition`
from transcriber import WhisperModel
# Load ground truth sentences
with open('/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/Audio_pipeline_test/ground_truth.txt', 'r') as file:
    ground_truth_sentences = [line.strip() for line in file.readlines()]



# Function to transcribe audio using STT algorithm
def transcribe_audio(file_path):
    model= WhisperModel(model_size_or_path="base.en", device="cpu", compute_type="int8")
    try:
        transcription,_ = model.transcribe(audio=file_path, language="en",without_timestamps=True)
    except sr.UnknownValueError:
        transcription = ""
    return transcription[0].text

# Function to calculate WER
def calculate_wer(reference, hypothesis):
    return wer(reference, hypothesis)

# Function to process each configuration folder
def process_configuration_folder(folder_path):
    results = []
    audio_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.wav')])
    for idx, file in enumerate(audio_files):
        ground_truth = ground_truth_sentences[idx]
        file_path = os.path.join(folder_path, file)
        transcription = transcribe_audio(file_path)
        error_rate = calculate_wer(ground_truth, transcription)
        results.append([ground_truth, transcription, error_rate])
    return results

# Paths to the outer folders
outer_folders = [
    '/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/Audio_pipeline_test/Microphone Configurations',
    '/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/Audio_pipeline_test/VAD Configurations'
]

# Process each outer folder
for outer_folder in outer_folders:
    for configuration_folder in os.listdir(outer_folder):
        configuration_folder_path = os.path.join(outer_folder, configuration_folder)
        if os.path.isdir(configuration_folder_path):
            results = process_configuration_folder(configuration_folder_path)
            output_csv_path = os.path.join(configuration_folder_path, 'results.csv')
            with open(output_csv_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Ground Truth', 'Transcription', 'WER'])
                csvwriter.writerows(results)
