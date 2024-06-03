import os
import sys
import json
from openai import AzureOpenAI
from tools import TOOLS

filepath=os.path.abspath(os.getcwd())
sys.path.append(filepath)
#A tool call can only be made by the user,not by AI guessing. If the user tries to request a tool call with an argument not found in the enum list of the tool, you must ask the user for a correct argument. Tools are only allowed to be called with the arguments specified in the given tool's enum list.

class ChatGPT():
    def __init__(self):
        self.functions = TOOLS
        self.messages =[]
        self.read_config('/home/rasmus/Desktop/Master/MasterThesisGit/OldTestCode/ChatGPT/chat_config.json')
        
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
                model="gpt-35-turbo", 
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

    def response_handler(self,response):

        msg = response.choices[0].message
        print(response.choices)

        # Check if the is a message responseg
        if msg.content is not None:
            # This should be stored in blackbord for the TTS
            print("MSG: "+msg.content)

        # Checks if functions needs to be called
        if msg.tool_calls is not None:
            print ("TOOLS: "+str(msg.tool_calls))

            tool_calls = msg.tool_calls
            if tool_calls:
                if msg.content is None:
                    msg.content = "" # required due to a bug in the SDK. We cannot send a message with None content
                for tool_call in tool_calls:
                #    # we may get a request to call more than one function(!)
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    print(function_name)
                    print(function_args)
                #    if function_name == 'call_rest_api':
                #        # Here, we call the requested function and get a response as a string
                #        function_response = self.call_rest_api(function_args)
                #        # We add the response to messages
                #        self.messages.append({
                #            "tool_call_id": tool_call.id,
                #            "role": "tool",
                #            "name": function_name,
                #            "content": function_response
                #        })

                #        self.call_ai(new_message=None)
        #self.messages.append(response)

    def get_last_message(self):
        return self.messages[-1]
    
    def print_message(self):
        try:
            msg = self.get_last_message()
            if msg is not None:
                print(msg)
        
        except Exception as e:
            print(e)

def main(args=None):
    # Main loop to chat with GPT
    AI = ChatGPT()
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ChatGPT: Goodbye!")
            break
        
        # Should be the input from the STT stored in the 
        message=user_input

        # Get the assistant's response
        response=AI.chat_with_gpt(message)

        AI.response_handler(response)

        # Extract the assistant's reply from the response
        assistant_reply = AI.get_last_message()

        # Add the assistant's response to the conversation history
        AI.messages.append(assistant_reply)

        # Print the assistant's response
        #print(f"ChatGPT: {assistant_reply}")

if __name__ == '__main__':
    main()
