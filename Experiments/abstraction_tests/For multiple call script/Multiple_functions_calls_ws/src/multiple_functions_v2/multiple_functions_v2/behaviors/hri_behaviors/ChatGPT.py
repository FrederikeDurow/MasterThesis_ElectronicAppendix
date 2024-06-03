import os
import json
import logging
import py_trees
import threading
from threading import Event
from openai import AzureOpenAI, OpenAI
from py_trees.common import Status
from multiple_functions_v2.config.chatgpt_tools import TOOLS
import time

# Global Variables 
assistant_reply = ""
all_tools = []

class ChatGPT(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.event = Event()
            current_path = os.getcwd()
            config_path = os.path.join(current_path, "src/multiple_functions_v2/multiple_functions_v2/config/chatGPT_config.json")
            self.config = self.read_config(config_path)
            self.conversation = self.conversation = [{'role': 'system', 'content': self.config['system']}]



        except Exception as e:
            self.logger.error(str(e))
            
        
        
    def initialise(self) -> None:
        try: 
            global assistant_reply, all_tools
            all_tools = []
            assistant_reply = ""
            self.thread = None
            self.event.clear()
            py_trees.blackboard.Blackboard.set("LED_COLOR","YELLOW")
            self.first_run = True
            reset = py_trees.blackboard.Blackboard.get("chatgpt/reset")
            if reset:
                system_message = self.config['system']
                # Initialize the conversation history with the system message
                self.conversation = [{'role': 'system', 'content': system_message}]
                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", self.conversation)
            self.response = ""
            py_trees.blackboard.Blackboard.set("chatgpt/reset", False)
        except Exception as e:
            self.logger.error(str(e))

    def update(self) -> Status:
        try:
            py_trees.blackboard.Blackboard.set("LED_COLOR", "YELLOW")
            self.logger.info("Update: ChatGPT") 
            # run_flag = py_trees.blackboard.Blackboard.get("first_run") 
            # if run_flag == False:
            if self.first_run == True:
                self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                user_input = py_trees.blackboard.Blackboard.get("hri/text_command") # Tømmerløsning, listen_to_command inverter skal kigges på 

                self.logger.info("User Input: %s", user_input)

                py_trees.blackboard.Blackboard.set("hri/text_command", "")
                py_trees.blackboard.Blackboard.set("hri/function_returns","") #NOT SURE IF BELOW IS EVEN NEEDED AS THIS IS DONE IN THE BEHAVIORS THEMSELF RIGHT?
                function_returns = py_trees.blackboard.Blackboard.get("hri/function_returns")
                self.thread = threading.Thread(target=chat_thread, args=(self.event, user_input, function_returns, self.conversation,self.client,self.logger,))
                self.thread.start()
                self.first_run = False
            else: 
                if not self.thread.is_alive():
                    global assistant_reply, all_tools
                    py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", self.conversation)
                    py_trees.blackboard.Blackboard.set("chatgpt/msg", assistant_reply)
                    py_trees.blackboard.Blackboard.set("chatgpt/function_call", all_tools)
                    py_trees.blackboard.Blackboard.set("ChatGPT_active", False) 
                    return py_trees.common.Status.SUCCESS

            return py_trees.common.Status.RUNNING
            # else:
            #     return py_trees.common.Status.SUCCESS
   

        except Exception as e:
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE
        
            

    def read_config(self, file_path):
        try:
            with open(file_path, 'r') as config_file:   
                config = json.load(config_file)
            return config
        except Exception as e:
            self.logger.error(str(e))
        return None
    
    def terminate(self, new_status: py_trees.common.Status) -> None:
        self.event.set()
        # if self.thread.is_alive():
        #     self.thread.join()
        return super().terminate(new_status)
    


def chat_thread(event, user_input, function_returns, conversation, client, logger):
    try:
        global assistant_reply, all_tools
        logger.info("Thread GPT")
        
        if len(function_returns) !=0:
            for i in range(len(function_returns)):
                if event.is_set():
                    break
                else:
                    function_id = function_returns[i].id
                    function_name = function_returns[i].function.name
                    result = "result"

                    conversation.append({"role": "function", "tool_call_id": function_id, 
                                            "name": function_name, 
                                            "content": result})
        # Add the user message to the conversation history
        if user_input != "":
            conversation.append({'role': 'user', 'content': user_input})
            user_input = ""
        logger.info("Conversation: %s", conversation)

        # API call to GPT-3
        start_time = time.time()
        response = client.chat.completions.create( 
            messages=conversation,
            model="gpt-4o-2024-05-13",   #"gpt-35-turbo",
            temperature=0.7, 
            max_tokens=800, 
            top_p=0.95,
            frequency_penalty=0, 
            presence_penalty=0, 
            stop=None,
            tools=TOOLS,
            tool_choice="auto"
        )
        #logger.info(response)
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Extract the reply, add to conversation history and
        if response.choices[0].message.content is not None:
            msg = response.choices[0].message.content
            assistant_reply = msg

            # Add the assistant's response to the conversation history
            conversation.append({'role': 'assistant', 'content': assistant_reply})
            # Save the answer
        
            logger.info("Chat answer: %s", assistant_reply)

        # all_tools = []
        if response.choices[0].message.tool_calls is not None:
            tools_to_call = response.choices[0].message.tool_calls
            for i in range(len(tools_to_call)):
                if event.is_set():
                    break
                else:
                    ###
                    #ADD HERE SO THE FUNCTION CALLS ARE ADDED TO CONVERSATION ASWELL!
                    #NOT TESTED YET!
                    conversation.append({
                                            "role": 'assistant',
                                            "function_call": {
                                                "name": tools_to_call[i].function.name,
                                                "arguments": tools_to_call[i].function.arguments,
                                            },
                                            "tool_call_id": tools_to_call[i].id,
                                            "content": None
                                        })
                    ###

                    all_tools.append(tools_to_call[i])
            
            # py_trees.blackboard.Blackboard.set("chatgpt/function_call", all_tools)
            logger.info("Tools: %s", all_tools)

        py_trees.blackboard.Blackboard.set("execution_time", execution_time)
        py_trees.blackboard.Blackboard.set("total_tokens", response.usage.total_tokens)
    except Exception as e:
        logger.error(str(e))

