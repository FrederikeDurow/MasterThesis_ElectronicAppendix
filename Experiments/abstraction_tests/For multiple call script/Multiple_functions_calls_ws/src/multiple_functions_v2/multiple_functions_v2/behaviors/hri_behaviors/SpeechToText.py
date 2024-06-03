import io
import os
import py_trees
import torch
import whisper
from queue import Queue
from datetime import datetime
from py_trees.common import Status
import speech_recognition as sr
from audio_common_msgs.msg import AudioData 
from std_msgs.msg import String
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import numpy as np
import logging
import numpy as np
from scipy.io.wavfile import write
import wave
import cProfile
import pstats
from .transcriber import WhisperModel
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp
import csv
import sys
import json  # Required for JSON parsing
import re

filepath=os.path.abspath(os.getcwd())
sys.path.append(filepath)

PERSON = "Rasmus"

class SpeechToText(py_trees.behaviour.Behaviour):

    def __init__(self, name: str, phrase_timeout: int, input_timeout: int, whisper_version: str, model: str, logger: logging.Logger, save_data: bool):
        super().__init__(name=name)
        try: 
            
            self.phrase_timeout=phrase_timeout 
            self.input_timeout=input_timeout
            self.logger = logger
            self.save_data = save_data
            hub_path = torch.hub.get_dir()
            model_path = os.path.join(hub_path, "snakers4_silero-vad_master")
            self.sal_model, _ = torch.hub.load(repo_or_dir=model_path,
                                model='silero_vad',
                                source='local',
                                force_reload=True)
            self.model = model
            self.whisper_version = whisper_version
            if self.whisper_version  == "Ori":
                self.audio_model = whisper.load_model(model)
            elif self.whisper_version  == "CT2":
                self.audio_model = WhisperModel(model_size_or_path=self.model, device="cpu", compute_type="int8")
            elif self.whisper_version  == "JAX":
                self.audio_model = FlaxWhisperPipline(checkpoint="openai/whisper-base.en",batch_size=1, dtype=jnp.bfloat16) #openai/whisper-tiny.en, openai/whisper-base.en, openai/whisper-small.en, openai/whisper-medium.en, 
            else:
                self.logger.error("Wrong whisper_version, please use Ori, CT2 or JAX")

        except Exception as e: 
            self.logger.error(str(e))

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.audioQueue = []
            if PERSON == "Rasmus":
                self.main_path = "/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests"
            elif PERSON == "Frederike":
                self.main_path = None

            self.line_num = 0
            self.file_lines_num = 0
            self.file_num = 0
            self.current_file_name = None

            self.sample_folder = self.main_path+"/Test_samples/Level_02/samples"
            self.solution_folder = self.main_path+"/Test_samples/Level_02/solutions"

            self.solution_files = sorted([filename for filename in os.listdir(self.solution_folder) if filename.endswith(".txt")])
            self.sample_files = sorted([filename for filename in os.listdir(self.sample_folder) if filename.endswith(".txt")])
            self.output_folder = self.main_path+"/Test_results/Level_02/"
            self.first_run = True
            #self.subsriber = self.node.create_subscription(String, '/chatgpt/input', self.callback, 10) # for user dummy
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  

        
    def initialise(self) -> None:
        try: 
            # Process live audio data in chunks
            py_trees.blackboard.Blackboard.set("spot_sleeping", False)

        except Exception as e: 
            self.logger.error(str(e))

    def update(self) -> py_trees.common.Status:
        try:
            self.logger.info("Update: Speech-to-text") 
            flag = py_trees.blackboard.Blackboard.get("STT_flag")
            self.logger.info("STT FLAG STATUS: %s", flag)
            if flag:
                if self.first_run == True:
                    # Reset conversation
                    py_trees.blackboard.Blackboard.set("chatgpt/reset", True)
                    if self.file_num != len(self.sample_files):
                        self.current_file_name= self.sample_files[self.file_num]
                        self.logger.info("Current sample file: %s out of %d sample files", self.current_file_name, len(self.sample_files) )
                        self.output_file = self.output_folder+self.current_file_name+"_result.csv"

                        self.sample_path = os.path.join(self.sample_folder, self.current_file_name)

                        self.output_csv_path = os.path.join(self.output_folder, self.current_file_name)  # Corrected path joining
                        self.output_csv_path = os.path.splitext(os.path.join(self.output_folder, self.current_file_name))[0] + '.csv'
                        with open(self.sample_path, 'r') as infile, open(self.output_csv_path, 'w', newline='') as outfile:
                            sample_reader = list(csv.reader(infile))  # Read and convert to list
                            writer = csv.writer(outfile)          
                            writer.writerow(["Input","Message", "Function_calls", "Function_arguments","Solution_arguments", "Results", "Final_message","Total Tokens","Execution Time"])
                            self.transcription = sample_reader[self.line_num][0]
                            self.logger.info("Length is: %s", len(sample_reader))
                            self.file_lines_num = len(sample_reader)

                        if len(self.transcription) != 0:
                            py_trees.blackboard.Blackboard.set("hri/text_command", self.transcription)
                            py_trees.blackboard.Blackboard.set("spot_waiting_for_command", False)
                            py_trees.blackboard.Blackboard.set("STT_flag", False)
                            self.first_run = False
                            self.logger.info("STT Return: SUCCESS") 
                            return py_trees.common.Status.SUCCESS
                        else:
                            self.logger.info("STT Return: RUNNING") 
                            return py_trees.common.Status.RUNNING
                    else:
                        self.logger.info("No more files")
                        sys.exit()
                    
                elif self.first_run == False:
                    self.logger.info("FIRST RUN FALSE")
                    if self.line_num < self.file_lines_num:

                        self.sample_path = os.path.join(self.sample_folder, self.current_file_name)

                        self.output_csv_path = os.path.join(self.output_folder, self.current_file_name)  # Corrected path joining
                        self.output_csv_path = os.path.splitext(os.path.join(self.output_folder, self.current_file_name))[0] + '.csv'

                        with open(self.sample_path, 'r') as infile, open(self.output_csv_path, 'a', newline='') as outfile:

                            self.solutionfile_name = self.solution_files[self.file_num]
                            self.logger.info("SOLUTION_FILE: %s", self.solutionfile_name)
                            self.solutionfile_path = os.path.join(self.solution_folder, self.solutionfile_name)
                        
                            solutionfile = open(self.solutionfile_path, 'r')
                            solution_reader = list(csv.reader(solutionfile))

                            sample_reader = list(csv.reader(infile))  # Read and convert to list                            writer = csv.writer(outfile)          
                            # writer.writerow(["Input","Message", "Function_calls", "Function_arguments", "Results","Completion Tokens","Prompt Tokens","Total Tokens","Execution Time"])

                            # Logic for writing to .csv file here
                            self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                            try:
                                # Extract user input
                                input = self.conversation[1]["content"]
                            except:
                                input = "None"

                            try:
                                # Extract ai msg
                                ai_msg = self.conversation[2]["content"]
                            except:
                                ai_msg= "None"

                            try:
                                behavior_msg = self.conversation[3]["content"]
                            except:
                                behavior_msg = "None"

                            try:
                                # Extract the final message
                                final_msg = self.conversation[-1]["content"]
                            except:
                                final_msg = "None"

                            # Extract function calls and function arguments
                            function_calls = []
                            function_args = []
                            for conversation_element in self.conversation:
                                # Extract the function call and arguments
                                if 'function_call' in conversation_element:
                                    func_call = conversation_element['function_call']
                                    function_calls.append(func_call['name'])
                                    function_args.append(func_call['arguments'])


                            # Parse JSON strings in function_args
                            parsed_function_args = [json.loads(arg) for arg in function_args]
                            function_arg_values = []
                            for arg_dict in parsed_function_args:
                                for value in arg_dict.values():
                                    function_arg_values.append(value)

                            try:
                                # Extract and check the results
                                result = py_trees.blackboard.Blackboard.get("Result")
                                if result != "ERROR":
                                    result = "FAILURE"
                                    solution_args = solution_reader[self.line_num]

                                    if re.search("[ERROR IN CALLING THE FUNCTION]", str(behavior_msg)) is None:
                                        # No functions were called but AI provided some message
                                        result = "CLARIFICATION"
                                        # Function are called and matches what is in solution file
                                    elif len(function_arg_values) == len(solution_args) and function_arg_values == solution_args:
                                        result = "SUCCESS"

                                    if len(function_arg_values) == 0 and final_msg != "None":
                                        result ="CLARIFICATION"
                                else:
                                    py_trees.blackboard.Blackboard.set("Result", "FAILURE")
                            except:
                                result ="CLARIFICATION"

                            # Get total tokens and execution time
                            exe_time = py_trees.blackboard.Blackboard.get("execution_time")
                            total_tokens = py_trees.blackboard.Blackboard.get("total_tokens")

                            # Updates the .csv file
                            self.logger.info("Writing to file: %s", self.output_csv_path)
                            writer = csv.writer(outfile) 
                            try:
                                writer.writerow([input,ai_msg, function_calls, function_args, solution_args,result,final_msg,total_tokens,exe_time])
                            except:
                                writer.writerow([input,ai_msg, "exeption", "exeption", solution_args,result,"exeption","exeption","exeption"])
                            self.line_num +=1
                            self.transcription = sample_reader[self.line_num][0]


                            # Reset conversation
                            py_trees.blackboard.Blackboard.set("chatgpt/reset", True)
                            #py_trees.blackboard.Blackboard.set("STT_flag", False)
                            #self.first_run = True
                        if len(self.transcription) != 0:
                            py_trees.blackboard.Blackboard.set("hri/text_command", self.transcription)
                            py_trees.blackboard.Blackboard.set("spot_waiting_for_command", False)
                            py_trees.blackboard.Blackboard.set("STT_flag", False)
                            self.first_run = False
                            self.logger.info("STT Return: SUCCESS") 
                            return py_trees.common.Status.SUCCESS
                        else:
                            self.logger.info("STT Return: RUNNING") 
                            return py_trees.common.Status.RUNNING
                        
                    # Takes the next file and resets the counters
                    elif self.file_num <= len(self.sample_files):
                        self.file_num += 1
                        self.line_num = 0
                        self.first_run = True
                        self.logger.info("Done with sample file: %s", self.current_file_name)


                    
            else:
                self.logger.info("STT Return: SUCCESS") 
                return py_trees.common.Status.SUCCESS
        except Exception as e: 
            self.line_num += 1
            self.logger.error(str(e)) 
            self.logger.info("STT Exception: FAILURE") 
            py_trees.blackboard.Blackboard.set("first_run", True)
            py_trees.blackboard.Blackboard.set("spot_sleeping", True)
            
        return py_trees.common.Status.FAILURE
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
     

    def callback (self, msg)-> None:
        try:
            if msg:
                self.transcription = msg.data
        except Exception as e: 
            self.logger.error(str(e))

     
