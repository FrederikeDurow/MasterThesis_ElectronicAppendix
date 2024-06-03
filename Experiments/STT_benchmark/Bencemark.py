import os
import pandas as pd
import speech_recognition as sr
import time
import psutil
import whisper
from transcriber import WhisperModel
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp
from jiwer import wer
from tqdm import tqdm
from huggingface_hub import snapshot_download
import torch
import zipfile
import torchaudio
from glob import glob
import torchaudio
import numpy as np
#https://github.com/m-bain/whisperX/issues/337

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

def load_audio_for_whisper(file_path, version):
    if version !="JAX":
        waveform, _ = torchaudio.load(file_path)  # Load the waveform and ignore sample rate
        waveform = waveform.numpy().astype(np.float32)
        return waveform.squeeze(0)  # Ensure it is a single channel (mono)
    else: 
        waveform, sample_rate = torchaudio.load(file_path)
        # Convert PyTorch tensor to NumPy array and ensure it's float32 for compatibility
        waveform = waveform.numpy().astype(np.float32).squeeze(0)  # Ensure it is a single channel (mono)
        return {'array': waveform, 'sampling_rate': sample_rate}
# Utility functions
def load_transcripts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return {line.split()[0]: " ".join(line.split()[1:]) for line in file.readlines()}
    
def sileroTTS_recognize(audio,file_path):
    audio = audio
    device = torch.device('cpu')  # Change to 'cuda' if GPU is available
    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_stt',
                                           language='en',
                                           device=device)
    (read_batch, split_into_batches, read_audio, prepare_model_input) = utils

    start_time = time.time()
    test_files = glob(file_path)  # Load audio file

    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                            device=device)
    output = model(input)
    transcription = ""
    for example in output:
        transcription=(decoder(example.cpu()))
    end_time = time.time()

    return transcription, end_time - start_time

# Google and Sphinx recognition functions
def google_recognize(audio,file_path):
    recognizer = sr.Recognizer()
    try:
        start_time = time.time()
        text = recognizer.recognize_google(audio)
        end_time = time.time()
        return text, end_time - start_time
    except sr.RequestError:
        return "API unavailable", 0
    except sr.UnknownValueError:
        return "Unable to recognize speech", 0

def sphinx_recognize(audio,file_path):
    recognizer = sr.Recognizer()
    try:
        start_time = time.time()
        text = recognizer.recognize_sphinx(audio)
        end_time = time.time()
        return text, end_time - start_time
    except sr.UnknownValueError:
        return "Unable to recognize speech", 0

# Whisper models initialization and transcription function
def initialize_whisper(version):
    if version == "Ori":
        return whisper.load_model("base")
    elif version == "CT2":
        return WhisperModel(model_size_or_path="base.en", device="cpu", compute_type="int8")
    elif version == "JAX":
        return FlaxWhisperPipline(checkpoint="openai/whisper-base.en", batch_size=1, dtype=jnp.bfloat16)
    
def whisper_ori_transcribe(audio,audio_path):
    sound = load_audio_for_whisper(audio_path,"Ori")
    model = initialize_whisper("Ori")
    start_time = time.time()
    result = model.transcribe(sound, fp16=False)
    end_time = time.time()
    return result['text'].strip(), end_time - start_time

def whisper_ct2_transcribe(audio,audio_path):
    sound = load_audio_for_whisper(audio_path,"CT2")
    model = initialize_whisper("CT2")
    start_time = time.time()
    result, _ = model.transcribe(language="en", without_timestamps=True, audio=sound)
    end_time = time.time()
    return result[0].text, end_time - start_time

def whisper_jax_transcribe(audio,audio_path):
    sound = load_audio_for_whisper(audio_path,'JAX')
    model = initialize_whisper("JAX")
    start_time = time.time()
    result = model(sound, language="en", task="transcribe")
    end_time = time.time()
    return result['text'].strip(), end_time - start_time

# def whisper_transcribe(audio, version):
#     try:
#         start_time = time.time()
#         if version == "Ori":
#             model = initialize_whisper()
#             result = model.transcribe(audio, fp16=False)
#         elif version == "CT2":
#             model = initialize_whisper()
#             result, _ = model.transcribe(language="en", without_timestamps=True, audio=audio)
#         elif version == "JAX":
#             model = initialize_whisper()
#             result = model(audio, language="en", task="transcribe")
#         end_time = time.time()
#         return result['text'].strip() if version != "CT2" else result[0].text, end_time - start_time
#     except Exception as e:
#         return str(e), 0

# Process each audio file
def process_audio(file_path, function, model=None, version=None):
    recognizer = sr.Recognizer()
    audio_path = file_path
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        audio_duration = source.DURATION


    # Metrics calculation
    transcription, elapsed_time = function(audio,audio_path) if not model else whisper_transcribe(audio,audio_path)
    real_time_factor = elapsed_time / audio_duration if audio_duration > 0 else float('inf')
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(interval=1)
    memory_usage = process.memory_info().rss / (1024 * 1024)  # in MB
    return transcription, elapsed_time, real_time_factor, cpu_usage, memory_usage

def benchmark_datasets(libri_path, vctk_path, output_dir):
    # Define algorithms
    algorithms = {
        'Google': google_recognize,
        'Silero': sileroTTS_recognize,
        'Whisper-Ori': whisper_ori_transcribe,
        'Whisper-CT2': whisper_ct2_transcribe,
        'Whisper-JAX': whisper_jax_transcribe,
    }

    # Prepare results storage
    results = {name: pd.DataFrame(columns=['Dataset', 'Filename', 'Algorithm', 'Transcription', 'GroundTruth',
                                           'ExecutionTime', 'RealTimeFactor', 'CPUUsage', 'MemoryUsage', 'WER'])
               for name in algorithms.keys()}

    # Iterate through VCTK directory (example, extend to LibriSpeech similarly)
    total_files = sum(len(files) for _, _, files in os.walk(vctk_path))
    progress = tqdm(total=total_files, desc='Processing VCTK', unit='file')
    txt_path = os.path.join(vctk_path, "txt")
    wav_path = os.path.join(vctk_path, "wav48_silence_trimmed")

    if not os.path.exists(txt_path) or not os.path.exists(wav_path):
        print(f"Error: One or more directories do not exist. \nCheck txt path: {txt_path} \nCheck wav path: {wav_path}")
        return

    for speaker_dir in os.listdir(txt_path):
        speaker_txt_path = os.path.join(txt_path, speaker_dir)
        speaker_wav_path = os.path.join(wav_path, speaker_dir)
        for transcript_file in os.listdir(speaker_txt_path):
            if transcript_file.endswith(".txt"):
                txt_file_path = os.path.join(speaker_txt_path, transcript_file)
                audio_base = transcript_file[:-4]  # remove '.txt' from filename
                for mic in ["mic1", "mic2"]:
                    audio_file_path = os.path.join(speaker_wav_path, f"{audio_base}_{mic}.flac")
                    if os.path.exists(audio_file_path):
                        with open(txt_file_path, 'r', encoding='utf-8') as f:
                            transcript = f.read().strip()
                        for algo_name, func in algorithms.items():
                            try:
                                transcription, elapsed_time, rtf, cpu_usage, memory_usage = process_audio(audio_file_path, func)
                                error_rate = wer(transcript.lower(), transcription.lower())
                            except Exception as e:
                                transcription = "ERROR"
                                elapsed_time = rtf = cpu_usage = memory_usage = error_rate = None
                                print(f"Error processing {audio_file_path} with {algo_name}: {str(e)}")

                            results[algo_name] = results[algo_name].append({
                                'Dataset': 'VCTK',
                                'Filename': f"{audio_base}_{mic}",
                                'Algorithm': algo_name,
                                'Transcription': transcription,
                                'GroundTruth': transcript,
                                'ExecutionTime': elapsed_time,
                                'RealTimeFactor': rtf,
                                'CPUUsage': cpu_usage,
                                'MemoryUsage': memory_usage,
                                'WER': error_rate
                            }, ignore_index=True)
                        progress.update(1)

    progress.close()  # Close the progress bar when done

    # Save results to separate CSV files for each algorithm
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for algo_name, df in results.items():
        df.to_csv(os.path.join(output_dir, f"{algo_name}_results.csv"), index=False)

# Specify the paths and execute
libri_path = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/audio_dir/LibriSpeech/train-other-500'
vctk_path = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/audio_dir/VCTK'
output_dir = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/results_dir'
benchmark_datasets(libri_path, vctk_path, output_dir)



















# # Benchmark function
# def benchmark_datasets(libri_path, vctk_path, output_csv):
#     results = pd.DataFrame(columns=['Dataset', 'Filename', 'Algorithm', 'Transcription', 'GroundTruth', 'ExecutionTime', 'RealTimeFactor', 'CPUUsage', 'MemoryUsage', 'WER'])
    
#     # # Process LibriSpeech
#     # total_files = sum(len(files) for _, _, files in os.walk(libri_path))  # Calculate total files for progress bar setup
#     # progress = tqdm(total=total_files, desc='Processing LibriSpeech', unit='file')  # Setup progress bar

#     # for root, dirs, files in os.walk(libri_path):
#     #     for file in files:
#     #         if file.endswith(".trans.txt"):
#     #             transcripts = load_transcripts(os.path.join(root, file))
#     #             for audio_file, transcript in transcripts.items():
#     #                 audio_path = os.path.join(root, f"{audio_file}.flac")
#     #                 for algorithm in [google_recognize, sileroTTS_recognize]:
#     #                     try:
#     #                         transcription, elapsed_time, rtf, cpu_usage, memory_usage = process_audio(audio_path, algorithm)
#     #                         error_rate = wer(transcript.lower(), transcription.lower())
#     #                     except Exception as e:
#     #                         transcription = "ERROR"
#     #                         elapsed_time = rtf = cpu_usage = memory_usage = error_rate = None
#     #                         print(f"Error processing {audio_path} with {algorithm}: {str(e)}")

#     #                     results = results.append({
#     #                         'Dataset': 'LibriSpeech',
#     #                         'Filename': audio_file,
#     #                         'Algorithm': algorithm,
#     #                         'Transcription': transcription,
#     #                         'GroundTruth': transcript,
#     #                         'ExecutionTime': elapsed_time,
#     #                         'RealTimeFactor': rtf,
#     #                         'CPUUsage': cpu_usage,
#     #                         'MemoryUsage': memory_usage,
#     #                         'WER': error_rate
#     #                     }, ignore_index=True)
                    
#     #                 # Whisper algorithms
#     #                 for version in ['Ori', 'CT2', 'JAX']:
#     #                     try:
#     #                         model = initialize_whisper(version)
#     #                         transcription, elapsed_time, rtf, cpu_usage, memory_usage = process_audio(audio_path, whisper_transcribe, model, version)
#     #                         error_rate = wer(transcript.lower(), transcription.lower())
#     #                     except Exception as e:
#     #                         transcription = "ERROR"
#     #                         elapsed_time = rtf = cpu_usage = memory_usage = error_rate = None
#     #                         print(f"Error processing {audio_path} with {algorithm}: {str(e)}")

#     #                     results = results.append({
#     #                         'Dataset': 'LibriSpeech',
#     #                         'Filename': audio_file,
#     #                         'Algorithm': algorithm,
#     #                         'Transcription': transcription,
#     #                         'GroundTruth': transcript,
#     #                         'ExecutionTime': elapsed_time,
#     #                         'RealTimeFactor': rtf,
#     #                         'CPUUsage': cpu_usage,
#     #                         'MemoryUsage': memory_usage,
#     #                         'WER': error_rate
#     #                     }, ignore_index=True)
#     #                 progress.update(1)

#     # progress.close()  # Close the progress bar when done

#     # Process VCTK similarly, adjust paths and function calls accordingly

#     total_files = sum(len(files) for _, _, files in os.walk(vctk_path))  # Calculate total files for progress bar setup
#     progress = tqdm(total=total_files, desc='Processing VCTK', unit='file')  # Setup progress bar

#     txt_path = os.path.join(vctk_path, "txt")
#     wav_path = os.path.join(vctk_path, "wav48_silence_trimmed")
#     if not os.path.exists(txt_path) or not os.path.exists(wav_path):
#         print(f"Error: One or more directories do not exist. \nCheck txt path: {txt_path} \nCheck wav path: {wav_path}")
#     else:
#         for speaker_dir in os.listdir(txt_path):
#             speaker_txt_path = os.path.join(txt_path, speaker_dir)
#             speaker_wav_path = os.path.join(wav_path, speaker_dir)
#             for transcript_file in os.listdir(speaker_txt_path):
#                 if transcript_file.endswith(".txt"):
#                     txt_file_path = os.path.join(speaker_txt_path, transcript_file)
#                     audio_base = transcript_file[:-4]  # remove '.txt' from filename to match the audio filename
#                     for mic in ["mic1", "mic2"]:
#                         audio_file_path = os.path.join(speaker_wav_path, f"{audio_base}_{mic}.flac")
#                         if os.path.exists(audio_file_path):
#                             with open(txt_file_path, 'r', encoding='utf-8') as f:
#                                 transcript = f.read().strip()
#                             for algo_name, func in {
#                                 'Google': google_recognize,
#                                 'Silero': sileroTTS_recognize,
#                                 'Whisper-Ori': whisper_ori_transcribe,
#                                 'Whisper-CT2': whisper_ct2_transcribe,
#                                 'Whisper-JAX': whisper_jax_transcribe,
#                             }.items():
#                                 try:
#                                     transcription, elapsed_time, rtf, cpu_usage, memory_usage = process_audio(audio_file_path, func)
#                                     error_rate = wer(transcript.lower(), transcription.lower())
#                                 except Exception as e:
#                                     transcription = "ERROR"
#                                     elapsed_time = rtf = cpu_usage = memory_usage = error_rate = None
#                                     print(f"Error processing {audio_file_path} with {algo_name}: {str(e)}")

#                                 results = results.append({
#                                     'Dataset': 'VCTK',
#                                     'Filename': f"{audio_base}_{mic}",
#                                     'Algorithm': algo_name,
#                                     'Transcription': transcription,
#                                     'GroundTruth': transcript,
#                                     'ExecutionTime': elapsed_time,
#                                     'RealTimeFactor': rtf,
#                                     'CPUUsage': cpu_usage,
#                                     'MemoryUsage': memory_usage,
#                                     'WER': error_rate
#                                 }, ignore_index=True)
#                             progress.update(1)
#     progress.close()  # Close the progress bar when done

#     # Save results to CSV
#     results.to_csv(output_csv, index=False)

# # Specify the paths and execute
# libri_path = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/audio_dir/LibriSpeech/train-other-500'
# vctk_path = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/audio_dir/VCTK'
# output_csv = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/results_dir'
# benchmark_datasets(libri_path, vctk_path, output_csv)