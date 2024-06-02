import json
import logging
import py_trees
from py_trees.common import Status 
from behavior_tree.config.chatgpt_tools import TOOLS


class BehaviorHandler(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
    
    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
            self.first_run = True
            self.functions_queue = []
            self.functions_errors = []
        except Exception as e:
            self.logger.error(str(e))
        
    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","YELLOW")
        self.functions_errors = []
        self.conversation = []

    def append_to_dict(self, id:str,function_name:str, value:str)->None:
        id_found = False
        for i in range(len(self.functions_errors)):
            if id in self.functions_errors[i]:
                self.functions_errors[i]["content"].append(value)
                id_found = True
        
        if id_found is False:
            temp = {"id": id, "function_name": function_name, "content": value}
            self.functions_errors.append(temp)

    def update(self) -> Status:
        try:
            self.first_run = py_trees.blackboard.Blackboard.get("first_run")
            if self.first_run == True:
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                try:
                    functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
                except:
                    functions_to_call=None

                
                if msg and not functions_to_call:
                    py_trees.blackboard.Blackboard.set("chatgpt/msg", "")
                    py_trees.blackboard.Blackboard.set("text_to_speak/talk",msg)
                    py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "enabled")
                    self.logger.info("BehaviorHandler: %s", msg)
                    return py_trees.common.Status.SUCCESS 

                ## Checks if there is a function to call ###########################################
                else:

                    for i in functions_to_call:

                        function_name = i.function.name

                        if function_name !="":
                            # Validate function 
                            tool = next((t for t in TOOLS if t["function"]["name"] == function_name), None)
                            if tool is None:
                                self.logger.error("Unknown function call: %s", function_name)
                                error = "Unknown function or tool to call: " + str(function_name)
                                self.append_to_dict(i.id,function_name,error)

                            else: 
                                # Validate the parameters
                                expected_parameters = tool["function"]["parameters"]
                                required_parameters = tool["function"]["parameters"]["required"]
                                actual_parameters = json.loads(i.function.arguments)

                                for key, value in expected_parameters["properties"].items():
                                    if key not in actual_parameters and key in required_parameters:
                                        self.logger.error("Missing required parameter: %s",key)
                                        error = "Missing required parameter: " + str(key)
                                        self.append_to_dict(i.id,function_name,error)
                                    try:
                                        if actual_parameters[key] != None:
                                            if "enum" in value:
                                                if actual_parameters[key] not in value["enum"]:
                                                    self.logger.error("Invalid value for parameter <{}>: {} is not a part of avalible options.".format(key, actual_parameters[key]))
                                                    error = "Invalid value for parameter {}: {}".format(key, actual_parameters[key])
                                                    self.append_to_dict(i.id,function_name,error)
                                    except:
                                        continue
                    #CHECK FOR ERRORS IN FUNCTION
                    if len(self.functions_errors) > 0:
                        # GO THROUGH THE ERRORS AND APPEND TO CONVERSATION.
                        self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        for i in range(len(self.functions_errors)):
                            msg={
                            "role": "function",
                            "tool_call_id": self.functions_errors[i]["id"],
                            "name": self.functions_errors[i]["function_name"],
                            "content":"[ERROR IN CALLING THE FUNCTION]: The reason for this is the following: "+ str(self.functions_errors[i]["content"]+". Please generate a short and precise message for the user with suggestions on a fix."),
                            }
                            self.conversation.append(msg)
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",self.conversation)
                        py_trees.blackboard.Blackboard.set("chatgpt/function_call","")
                        self.first_run = True
                        py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                        py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                        py_trees.common.Status.FAILURE
                    else:
                        self.first_run = False
                        py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                        py_trees.blackboard.Blackboard.set("ChatGPT_active", False)
                        self.functions_queue = functions_to_call
                        
            
            # CONTINUE PERFORMING THE FUNCTION CALLS
            if len(self.functions_queue) != 0 and self.first_run == False:
                # Check for conditions FD-NEW
                args=json.loads(self.functions_queue[0].function.arguments)
                try:
                    object_found_condition=args["object_found_condition"] 
                except: 
                    object_found_condition=None
                try:
                    current_location_condition=args["current_location_condition"]
                except: 
                    current_location_condition=None
                if object_found_condition is not None:
                    if py_trees.blackboard.Blackboard.get("object_found") != object_found_condition:
                        self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        chat_msg={
                            "role": "function",
                            "tool_call_id": self.functions_queue[0].id,
                            "name": self.functions_queue[0].function.name,
                            "content":"[INFO]: The following function was not called due to object_found not being "+str(object_found_condition)+".",
                            }
                        self.conversation.append(chat_msg)
                        self.functions_queue.pop(0)
                        if len(self.functions_queue) == 0:
                            self.logger.info("No more functions")
                            self.first_run = True
                            py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                            py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                            self.conversation[-1]["content"] += "This was the last function to call. Please generate a message to the user with feedback on how the execution of all functions went."
                            

                        self.logger.info("Condition false, function not called")
                        self.conversation[-1]["content"] += "The system will move on to the next function and try to execute that now."
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", self.conversation)
                        return py_trees.common.Status.SUCCESS 
                if current_location_condition is not None:
                    if py_trees.blackboard.Blackboard.get("current_location") != current_location_condition:
                
                        self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        chat_msg={
                            "role": "function",
                            "tool_call_id": self.functions_queue[0].id,
                            "name": self.functions_queue[0].function.name,
                            "content":"[INFO]: The following function was not called due to current_location not being "+str(current_location_condition)+".",
                            }
                        self.conversation.append(chat_msg)
                        
                        self.functions_queue.pop(0)
                        if len(self.functions_queue) == 0:
                            self.logger.info("No more functions")
                            self.first_run = True
                            py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                            py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                            self.conversation[-1]["content"] += "This was the last function to call. Please generate a message to the user with feedback on how the execution of all functions went."
                        self.logger.info("Condition false, function not called due to an location requirement condition not being fulfilled")
                        self.conversation[-1]["content"] += "The system will move on to the next function and try to execute that now."
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", self.conversation)
                        return py_trees.common.Status.SUCCESS 
                
               
                
                # add what to do if only one of them is not none
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                if msg:
                    py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg", True)

                py_trees.blackboard.Blackboard.set(str(self.functions_queue[0].function.name+"_behavior"), "enabled")
                py_trees.blackboard.Blackboard.set("function_id", self.functions_queue[0].id)
                py_trees.blackboard.Blackboard.set("chatgpt/function_call", [self.functions_queue[0]])
                self.logger.info("Condition True, function called.")
                self.functions_queue.pop(0)
       
                return py_trees.common.Status.SUCCESS
            
            elif len(self.functions_queue) == 0:
                self.logger.info("No more functions")
                self.first_run = True
                py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                self.conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                self.conversation[-1]["content"] +=  "Please generate a message to the user with an update on the execution results of all called functions"
                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", self.conversation)
                # All function have completed, return to ChatGPT
           
                return py_trees.common.Status.FAILURE
                      
        except Exception as e:
            self.logger.error("No behavior enabled because of exception: %s", e)
        
        return py_trees.common.Status.FAILURE

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
    