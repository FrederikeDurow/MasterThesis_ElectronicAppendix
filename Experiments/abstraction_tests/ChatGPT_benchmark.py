import os
import sys
import json
from openai import AzureOpenAI, OpenAI
from tools import TOOLS
import csv
import time
from tqdm import tqdm
import re
import logging

PERSON = "Rasmus" #Frederike

filepath=os.path.abspath(os.getcwd())
sys.path.append(filepath)
#A tool call can only be made by the user,not by AI guessing. If the user tries to request a tool call with an argument not found in the enum list of the tool, you must ask the user for a correct argument. Tools are only allowed to be called with the arguments specified in the given tool's enum list.

class ChatGPT():
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.functions = TOOLS
        self.messages =[]

        if PERSON == "Frederike":
            self.read_config('/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/chat_config.json')
        elif PERSON == "Rasmus":
            self.read_config('/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/chat_config.json')

        # self.client = AzureOpenAI(
        #     api_key="",
        #     api_version = "2023-12-01-preview",
        #     azure_endpoint = "https://robot-tsko-openai.openai.azure.com/")

        self.client = OpenAI(
                api_key = "")
        
        self.known_objects = ["banana", "apple", "cup", "laptop", "dog", "cat", "bottle", "teddy bear", "person", "bowl", "refrigerator"]
        self.known_locations = ["home","garage","garden","office","bedroom","kitchen","workshop","dining room","living room"]
        
    # Function to read and parse the configuration file
    def read_config(self,file_path):
        try:
            with open(file_path, 'r') as config_file:
                config = json.load(config_file)

            if config and 'system' in config:
                system_message = config['system']

            # Initialize the conversation history with the system message
                self.messages.append({'role': 'system', 'content': system_message})
            else: 
                self.messages.append({'role': 'system', 'content': 'You are a helpful assistant.'})

        except Exception as e:
            print(f"Error reading config file: {e}")
            return None
    
    # Function to interact with ChatGPT
    def chat_with_gpt(self,prompt):
        try:
            self.messages.append({'role': 'user', 'content':prompt})
            # Make an API call to chat with GPT-3
            response = self.client.chat.completions.create( 
                model="gpt-4o-2024-05-13", 
                #response_format={ "type": "json_object" },
                messages = self.messages, 
                temperature=0.7, 
                max_tokens=800, 
                top_p=0.95,
                frequency_penalty=0, 
                presence_penalty=0, 
                stop=None,
                tools=TOOLS,
                tool_choice="auto"
            )
            return response
            # Extract and return the generated text from the response
        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_sentences(self,level, filename, sample_file,solution_file, output_file):
          with open(sample_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            if solution_file is not None: 
                solutionfile = open(solution_file, 'r')
                solution_reader = csv.reader(solutionfile)

            sample_reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Write header to the CSV file
            # if level == "Level_00" or level == "Level_01":
            writer.writerow(["Input","Message", "Function_calls", "Function_arguments", "Results","Completion Tokens","Prompt Tokens","Total Tokens","Execution Time"])

            # Count the total number of lines in the file
            total_lines = sum(1 for line in infile)

            # Reset file pointer to the beginning of the file
            infile.seek(0)

            # Initialize tqdm with the total number of lines
            with tqdm(total=total_lines, desc=f"Processing {sample_file}") as pbar:
                counter = 0
                for row in sample_reader:
                    try:
                        if row:  # Check if the row is not empty
                            input_sentence = row[0]

                            start_time = time.time()
                            response = self.chat_with_gpt(input_sentence)
                            end_time = time.time()
                            execution_time = end_time - start_time

                            msg = response.choices[0].message
                            if msg.content is not None:
                                text = msg.content
                            else:
                                text = "" #fd

                            tool_calls = msg.tool_calls
                            function_names =[]
                            function_arguments =[]
                            if tool_calls:
                                if msg.content is None:
                                    msg.content = "" # required due to a bug in the SDK. We cannot send a message with None content
                                for tool_call in tool_calls:
                                    function_name = tool_call.function.name
                                    function_args = tool_call.function.arguments

                                    function_names.append(function_name)
                                    function_arguments.append(function_args)

                            self.messages.pop()
                            # Check if result is correct 
                            result = "FAILURE"
                            if level == "Level_00" or level == "Level_01" or level =="Level_04":
                                # Check Question Responses
                                if re.search('Answer', filename):
                                    if text != "" and function_names is [] and function_arguments is []:
                                        result = "SUCCESS"
                                # Check Location Tasks
                                elif re.search('Locate', filename):
                                    if text == "" and len(function_names) == 1 and len(function_arguments) == 1: # In level 0 and 1 there should not be any conditions or go_through locations
                                        for object in self.known_objects:
                                            if re.search(object, filename):
                                                if re.search(object, function_args.lower()):
                                                    result = "SUCCESS"
                                                break

                                # Check Navigation Tasks
                                elif re.search('Navigate', filename):
                                    if text == "" and len(function_names) == 1 and len(function_arguments) == 1: # In level 0 and 1 there should not be any conditions or go_through locations
                                        for location in self.known_locations:
                                            if re.search(location, filename):
                                                if re.search(location, function_args.lower()):
                                                    result = "SUCCESS"
                                                break
                                # Check if there is a msg instead (hence CLARIFICATION)
                                if result == "FAILURE" and text !="":
                                    result = "CLARIFICATION"
                            
                            elif level == "Level_02":
                                solution_row = solution_reader[counter]
                                counter+=1
                                solutions = solution_row.split(",")
                                result = "SUCCESS"

                                # In level 2 there should not be any text messages, conditions or go_through locations
                                if (text != "" or
                                    re.search('go_through_areas', function_args.lower()) or 
                                    re.search('object_found_condition', function_args.lower()) or 
                                    re.search('current_location_condition', function_args.lower()) or 
                                    len(solutions) != len(function_args)):
                                    result = "FAILURE"
                                   
                                else:
                                    # If one of the requested objectives does not match, it is a failure
                                    for s in range(len(solutions)):
                                        if not re.search(solutions[s], function_args[s].lower()):
                                            result = "FAILURE"
                                            break
                                
                            # Append the input and response to the CSV file
                            writer.writerow([input_sentence, text, function_names,function_arguments, result,response.usage.completion_tokens,response.usage.prompt_tokens,response.usage.total_tokens, execution_time])
                    except Exception as e: 
                           self.logger.error(str(e))                
                           writer.writerow(["ERROR"])      
                    # Update the progress bar
                    pbar.update(1)


def createLogger():
    logger = logging.getLogger("AbstractionLog")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')

    if PERSON == "Frederike":
        filehandler = logging.FileHandler("/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/abstraction_test.log")
    elif PERSON == "Rasmus":
        filehandler = logging.FileHandler("/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/abstraction_test.log")

    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger

if __name__ == "__main__":
    logger = createLogger()
    AI = ChatGPT(logger)

    level = "Level_00"
    logger.info("Abstraction %s", level)
  
    if level == "Level_02":
        if PERSON == "Frederike":
            sample_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/samples"
            solution_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/solutions"
        
        elif PERSON == "Rasmus":
            sample_folder = "/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/samples"
            solution_folder = "/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/solutions"

    else: 
        if PERSON == "Frederike":
            sample_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/"+level
            solution_folder = None
        elif PERSON == "Rasmus":
            sample_folder = "/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/Test_samples/"+level
            solution_folder = None
            
    # Sets the output folder
    if PERSON == "Frederike":
        output_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_results/GPT4/"+level
    elif PERSON == "Rasmus":
        output_folder = "/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/abstraction_tests/Test_results/GPT4/"+level

    # Get a list of files ending with '.txt'
    sample_files = [filename for filename in os.listdir(sample_folder) if filename.endswith(".txt")]

    if solution_folder is not None: 
        solution_files = [filename for filename in os.listdir(output_folder) if filename.endswith(".txt")]
    else:
        solution_files = None

     # Initialize tqdm with the total number of files
    with tqdm(total=len(sample_files), desc="Processing") as pbar:
        # Iterate over each txt file
        for i in range(len(sample_files)):
            sample_filename = sample_files[i]
            solution_path = None
            
            if solution_files is not None: 
                solution_filename = solution_files[i]
                solution_path = os.path.join(solution_folder, solution_filename)

            logger.info("Current file: %s", sample_filename)
            sample_path = os.path.join(sample_folder, sample_filename)

            output_csv_path = os.path.join(output_folder, sample_filename)  # Corrected path joining
            output_csv_path = os.path.splitext(os.path.join(output_folder, sample_filename))[0] + '.csv'

            # Process the sentences
            AI.process_sentences(level, sample_filename, sample_path, solution_path,  output_csv_path)
            
            # Update the progress bar
            pbar.update(1)
