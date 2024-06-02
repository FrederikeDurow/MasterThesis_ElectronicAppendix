import os
import json
import logging
import py_trees
import threading
from threading import Event
from openai import AzureOpenAI
from py_trees.common import Status
from behavior_tree.config.chatgpt_tools import TOOLS

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
            config_path = os.path.join(current_path, "src/behavior_tree/behavior_tree/config/chatGPT_config.json")
            self.config = self.read_config(config_path)
            self.conversation = self.conversation = [{'role': 'system', 'content': self.config['system']}]
        
            self.client = AzureOpenAI(
                api_key="", # add access key
                api_version = "2024-02-15-preview",
                azure_endpoint = "https://robot-tsko-openai.openai.azure.com/"
            )
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
                self.logger.info("Resetting the ChatGPT conversation")
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
        
            if self.first_run == True:
                self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                user_input = py_trees.blackboard.Blackboard.get("input_text_command") # Tømmerløsning, listen_to_command inverter skal kigges på 

                self.logger.info("User Input: %s", user_input)

                py_trees.blackboard.Blackboard.set("input_text_command", "")
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
        return super().terminate(new_status)
    


def chat_thread(event, user_input, function_returns, conversation, client, logger):
    try:
        global assistant_reply, all_tools
        
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
        response = client.chat.completions.create( 
            messages=conversation,
            model="gpt-35-turbo",
            temperature=0.7, 
            max_tokens=800, 
            top_p=0.95,
            frequency_penalty=0, 
            presence_penalty=0, 
            stop=None,
            tools=TOOLS,
            tool_choice="auto"
        )
        logger.info(response)
        
        # Extract the reply, add to conversation history and
        if response.choices[0].message.content is not None:
            msg = response.choices[0].message.content
            assistant_reply = msg

            # Add the assistant's response to the conversation history
            conversation.append({'role': 'assistant', 'content': assistant_reply})
            logger.info("Chat answer: %s", assistant_reply)

        if response.choices[0].message.tool_calls is not None:
            tools_to_call = response.choices[0].message.tool_calls
            for i in range(len(tools_to_call)):
                if event.is_set():
                    break
                else:
                    conversation.append({
                                            "role": 'assistant',
                                            "function_call": {
                                                "name": tools_to_call[i].function.name,
                                                "arguments": tools_to_call[i].function.arguments,
                                            },
                                            "tool_call_id": tools_to_call[i].id,
                                            "content": None
                                        })
                    all_tools.append(tools_to_call[i])
            
            logger.info("Tools: %s", all_tools)
    except Exception as e:
        logger.error(str(e))

