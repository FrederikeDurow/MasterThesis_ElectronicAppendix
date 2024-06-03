import torch
import time
from TTS.api import TTS
import soundfile as sf  # to read audio file duration
import pvorca
from io import BytesIO
import pyaudio
import wave
import struct
from mimic3_tts import Mimic3Settings, Mimic3TextToSpeechSystem
import wave
import psutil
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
from dimits import Dimits
from transformers import FastSpeech2ConformerTokenizer, FastSpeech2ConformerWithHifiGan
import subprocess
from TTS.utils.synthesizer import Synthesizer
from scipy.io.wavfile import write
import parselmouth
import numpy as np
import librosa
from scipy.signal import find_peaks

def calculate_hnr(sound_file):
    sound = parselmouth.Sound(sound_file)
    # Compute the harmonicity (HNR) using Praat's 'To Harmonicity (cc)' method
    harmonicity = sound.to_harmonicity_cc()
    
    # Access the harmonicity values and compute the mean HNR, ignoring undefined values (NaN)
    hnr_values = harmonicity.values[harmonicity.values != -200]  # Praat uses -200 to indicate undefined HNR values
    if len(hnr_values) > 0:  # Check if there are any valid HNR values
        mean_hnr = np.mean(hnr_values)
        return mean_hnr
    else:
        return None  # Return None if no valid HNR values exist



def calculate_cpp(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Compute the magnitude spectrum of the signal
    magnitude_spectrum = np.abs(np.fft.rfft(y))
    
    # Compute the log spectrum
    log_spectrum = np.log(magnitude_spectrum + np.finfo(float).eps)  # Add eps for numerical stability
    
    # Compute the real cepstrum
    real_cepstrum = np.fft.irfft(log_spectrum)
    
    # Find peaks in the cepstrum
    peaks, properties = find_peaks(real_cepstrum, prominence=(None, None))
    
    if len(peaks) == 0:
        print("No peaks found in cepstrum.")
        return None
    
    # The first peak is usually the most prominent in voice signals
    if 'prominences' in properties:
        peak_prominence_value = properties['prominences'][0]  # Access the first peak's prominence
        return peak_prominence_value
    else:
        return 0  # Return 0 if no prominences were calculated

def calculate_ltas(sound_file):
    # Load the sound file with parselmouth
    sound = parselmouth.Sound(sound_file)
    
    # Compute the spectrum
    spectrum = sound.to_spectrum()
    
    # Calculate the average of the power spectra (LTAS)
    # Power spectrum is square of the absolute values of the spectrum
    power_spectrum = np.square(np.abs(spectrum.values))
    
    # Average across time to compute LTAS
    ltas = np.mean(power_spectrum, axis=1)  # Assuming axis 1 is the time axis; adjust as needed
    ltas_mean = np.mean(ltas)
    
    return ltas_mean


# Paths
generated_audio_folder_path = "/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/Generated_audio/"
csv_folder_path = "/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/csv_files/"
text_sample_file_path = "/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/test_sample_real.txt"

# Load test samples
with open(text_sample_file_path, 'r') as file:
    test_samples = file.readlines()

# List of TTS algorithms
#TTS_algorithm_list = ["Mimic3", "Orca", "Parler", "Piper", "SileroTTS", "Cucu_tacotron2", "FastSpeech2","espeakNG", "MorzillaTTS"]
TTS_algorithm_list = ["Cucu_tacotron2"]

# Initialize CSV file
csv_header = "Algorithm, Sentence_Index, Word_Count, Execution_Time, Realtime_Factor, Duration_Consistency, CPU_Usage, Memory_Usage, HNR, CPP, LTAS\n"
for algorithm in TTS_algorithm_list:
    with open(f"{csv_folder_path}{algorithm}.csv", "w") as csv_file:
        csv_file.write(csv_header)


# Average spoken words per second (can vary based on language and context)
average_words_per_second = 2.5  # This is a common average value for natural speech


# Testing each algorithm
for algorithm in TTS_algorithm_list:

    if algorithm == "Orca":
        orca = pvorca.create(access_key="px6MFm1HSRLrFsNmBzvRT4GAGd30CPaNdV/czEsf9C+eZHpr7O5NOQ==",model_path="/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/TTS/orca_params_male.pv")

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"


            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            orca.synthesize_to_file(text=line_count, output_path=audio_file_path)

            end_time = time.time()

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0

            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "Mimic3":
        settings = Mimic3Settings(voice="en_US/cmu-arctic_low",  # info here
            voices_directories=None, #Directories to search for voices (<lang>/<voice>)
            speaker=8, # Default speaker name or id
            language="en_US",  # Set the language (if not using default)
            volume=100,  # Set the volume (0-100)
            rate=0.8,  # Set the speaking rate (adjust as needed)pi
            providers="CPUExecutionProvider",   # Other options: 'AzureExecutionProvider', 'CUDAExecutionProvider'
            no_download=True )# download voices automatically)# download voices automatically)
        # Create an instance of the Mimic3TextToSpeechSystem
        tts = Mimic3TextToSpeechSystem(settings)

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used
            audio_bytes=tts.text_to_wav(line_count)

            with wave.open(audio_file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # Sample width 2 bytes (16 bits)
                wav_file.setframerate(22050)  # Sample rate 22050 Hz
                wav_file.writeframes(audio_bytes)

            end_time = time.time()

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0

            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "Cucu_tacotron2":
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tts = TTS("tts_models/en/ek1/tacotron2").to(device)

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            try:
                tts.tts_to_file(text=line, file_path=audio_file_path)

                # Record CPU and memory after processing
                cpu_end = psutil.cpu_percent(interval=1)
                mem_end = psutil.virtual_memory().used
                end_time = time.time()

                execution_time = end_time - start_time
                cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
                memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

                # Estimate expected duration
                expected_duration = word_count / average_words_per_second

                # Estimate realtime factor using audio duration
                audio_data, sample_rate = sf.read(audio_file_path)
                audio_duration = len(audio_data) / sample_rate
                realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

                hnr_val = calculate_hnr(audio_data)
                cpp_val = calculate_cpp(audio_file_path)
                ltas_val = calculate_ltas(audio_data)

                # Calculate duration consistency
                duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


                # Write results to CSV
                with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                    csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")
            except:
                 # Write results to CSV
                with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                    csv_file.write(f"{algorithm}, {index}\n")

    elif algorithm == "SileroTTS":
        language = 'en'
        model_id = 'v3_en'
        sample_rate = 48000
        speaker = 'en_0'
        device = torch.device('cpu')

        model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
        model.to(device)  # gpu or cpu

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            audio = model.apply_tts(text=line_count,speaker=speaker,sample_rate=sample_rate)
            sf.write(audio_file_path, audio, sample_rate)

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "Parler":
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
        tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            prompt = line
            description = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, clear audio quality. He speaks very clearly"

            input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
            prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
            audio_arr = generation.cpu().numpy().squeeze()
            sf.write(audio_file_path, audio_arr, model.config.sampling_rate)

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "Piper":
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Initialize Dimits with the desired voice model
        dt = Dimits("en_US-ryan-high")

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_name = f"{algorithm}_{index}"
            audio_file_path = f"{generated_audio_folder_path}{audio_file_name}"  # Construct the full path


            start_time = time.time()
            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            dt.text_2_audio_file(line, audio_file_name, generated_audio_folder_path, format="wav")

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path+".wav")
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path+".wav")
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "FastSpeech2":

        tokenizer = FastSpeech2ConformerTokenizer.from_pretrained("espnet/fastspeech2_conformer")
        model = FastSpeech2ConformerWithHifiGan.from_pretrained("espnet/fastspeech2_conformer_with_hifigan")

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()

            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            inputs = tokenizer("Hello, my dog is cute.", return_tensors="pt")
            input_ids = inputs["input_ids"]

            output_dict = model(input_ids, return_dict=True)
            waveform = output_dict["waveform"]

            sf.write(audio_file_path, waveform.squeeze().detach().numpy(), samplerate=22050)

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "espeakNG":

        def synthesize_to_wav(text, filename):
            command = ['espeak', text, '--stdout']
            with open(filename, 'wb') as f:
                subprocess.run(command, stdout=f)

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()

            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            synthesize_to_wav(line.strip(), audio_file_path)

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")

    elif algorithm == "MorzillaTTS_not_working":

        synthesizer = Synthesizer('tts_models/en/ljspeech/tacotron2-DDC', 'vocoder_models/en/ljspeech/multiband-melgan')

        for index, line in enumerate(test_samples):
            line_count = line.strip()
            word_count = len(line_count.split())
            audio_file_path = f"{generated_audio_folder_path}{algorithm}_{index}.wav"

            start_time = time.time()

            # Record CPU and memory before processing
            cpu_start = psutil.cpu_percent(interval=1)
            mem_start = psutil.virtual_memory().used

            # Generate speech
            wav = synthesizer.tts(line)
            write('output_mozilla.wav', 22050, wav.numpy())

            # Record CPU and memory after processing
            cpu_end = psutil.cpu_percent(interval=1)
            mem_end = psutil.virtual_memory().used
            end_time = time.time()

            execution_time = end_time - start_time
            cpu_usage = cpu_end - cpu_start  # Compute the difference in CPU usage
            memory_usage = (mem_end - mem_start) / (1024 ** 2)  # Convert bytes to megabytes

            # Estimate expected duration
            expected_duration = word_count / average_words_per_second

            # Estimate realtime factor using audio duration
            audio_data, sample_rate = sf.read(audio_file_path)
            audio_duration = len(audio_data) / sample_rate
            realtime_factor = execution_time / audio_duration if audio_duration > 0 else 0

            hnr_val = calculate_hnr(audio_data)
            cpp_val = calculate_cpp(audio_file_path)
            ltas_val = calculate_ltas(audio_data)

            # Calculate duration consistency
            duration_consistency = audio_duration / expected_duration if expected_duration > 0 else 0


            # Write results to CSV
            with open(f"{csv_folder_path}{algorithm}.csv", "a") as csv_file:
                csv_file.write(f"{algorithm}, {index}, {word_count}, {execution_time:.2f}, {realtime_factor:.2f}, {duration_consistency:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}, {cpp_val:.2f}, {hnr_val:.2f}, {ltas_val:.2f}\n")






# Placeholder for other algorithms
# Implement similar sections for other algorithms with their specific configurations





# Placeholder for other algorithms
# Implement similar sections for other algorithms with their specific configurations


