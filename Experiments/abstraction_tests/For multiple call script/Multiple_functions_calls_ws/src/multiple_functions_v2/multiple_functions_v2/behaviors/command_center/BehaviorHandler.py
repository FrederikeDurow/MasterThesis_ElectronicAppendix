import json
import os
import py_trees
import logging
from py_trees.common import Status 
from multiple_functions_v2.config.chatgpt_tools import TOOLS


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

        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        
    def initialise(self) -> None:
        py_trees.blackboard.Blackboard.set("LED_COLOR","YELLOW")
        self.functions_errors = []

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
        # NEEDS MODIFICATION LATER ON!!!!
        # On top of this we need to have 2 talk to operator. Because sometime chatgpt also generate a msg with a function call.
            # Hence we need one check with only msg and one with msg and behavior call.
            # This could maybe be added as another parameter to the behavior.
            # Such that it have a standard sentence to say but replace with the msg if there is any. 
        try:
            self.logger.info("Update: Behavior Handler")
            self.first_run = py_trees.blackboard.Blackboard.get("first_run")
            if self.first_run == True:
                self.logger.info("BEHAVIOR HANDLER FIRST RUN")
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                try:
                    functions_to_call= py_trees.blackboard.Blackboard.get("chatgpt/function_call")
                except:
                    functions_to_call=None

                #Needs to add that it checks for function call
                #Because if not function then it should not perform the 

                if msg and not functions_to_call:
                    self.logger.info("Behavior Handler: msg but not functions to call")
                    py_trees.blackboard.Blackboard.set("chatgpt/msg", "")
                    py_trees.blackboard.Blackboard.set("text_to_speak/talk",msg)
                    py_trees.blackboard.Blackboard.set("talk_to_operator_behavior", "enabled")
                    self.logger.info("BehaviorHandler: %s", msg)
                    self.first_run = True
                    py_trees.blackboard.Blackboard.set("first_run", True)
                    py_trees.blackboard.Blackboard.set("STT_flag", True)
                    return py_trees.common.Status.SUCCESS 

                ## Checks if there is a function to call ###########################################
                else:

                    for i in functions_to_call:
                        #self.logger.info("I'th element of functions_to_call: %s", i)

                        function_name = i.function.name

                        if function_name !="":
                            tool = next((t for t in TOOLS if t["function"]["name"] == function_name), None)

                            # If the "called tool is not part of the TOOLS"
                            if tool is None:
                                self.logger.error("Unknown function call: %s", function_name)
                                error = "Unknown function or tool to call: " + str(function_name)
                                self.append_to_dict(i.id,function_name,error)
                                #return py_trees.common.Status.FAILURE

                            # Validate the parameters
                            expected_parameters = tool["function"]["parameters"]
                            required_parameters = tool["function"]["parameters"]["required"]
                            self.logger.info("required_parameters: %s", required_parameters)
                            actual_parameters = json.loads(i.function.arguments)
                            self.logger.info("actual_parameters: %s", actual_parameters )

                            for key, value in expected_parameters["properties"].items():
                                if key not in actual_parameters and key in required_parameters:
                                    self.logger.error("Missing required parameter: %s",key)
                                    error = "Missing required parameter: " + str(key)
                                    self.append_to_dict(i.id,function_name,error)
                                    #return py_trees.common.Status.FAILURE
                                try:
                                    if actual_parameters[key] != None:
                                        if "enum" in value:
                                            if actual_parameters[key] not in value["enum"]:
                                                self.logger.error("Invalid value for parameter <{}>: {} is not a part of avalible options.".format(key, actual_parameters[key]))
                                                error = "Invalid value for parameter {}: {}".format(key, actual_parameters[key])
                                                self.append_to_dict(i.id,function_name,error)
                                                #return py_trees.common.Status.FAILURE
                                except:
                                    continue
                    #CHECK FOR ERRORS IN FUNCTION
                    #self.logger.info(self.functions_errors)
                    if len(self.functions_errors) > 0:
                        # GO THROUGH THE ERRORS AND APPEND TO CONVERSATION.
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        for i in range(len(self.functions_errors)):
                            msg={
                            "role": "function",
                            "tool_call_id": self.functions_errors[i]["id"],
                            "name": self.functions_errors[i]["function_name"],
                            "content":"[ERROR IN CALLING THE FUNCTION]: The reason for this is the following: "+ str(self.functions_errors[i]["content"]+". Please generate a short and precise message for the user with suggestions on a fix."),
                            }
                            conversation.append(msg)
                        self.logger.info("I found all the errors, now i prepare for ChatGPTConversation")
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation",conversation)
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
                        
                        self.logger.info("Function call queue: %s", self.functions_queue)
            
            # CONTINUE PERFORMING THE FUNCTION CALLS
            if len(self.functions_queue) != 0 and self.first_run == False:
                self.logger.info("Checking for conditions")
                # Check for conditions FD-NEW
                args=json.loads(self.functions_queue[0].function.arguments)
                self.logger.info("Arguments: %s", args)
                try:
                    object_found_condition=args["object_found_condition"] # Take into consideration that it is a list
                except: 
                    object_found_condition=None
                try:
                    current_location_condition=args["current_location_condition"]
                except: 
                    current_location_condition=None
                #self.logger.info("object_found_condition: %s, current_location_condition: %s", object_found_condition, current_location_condition)
                if object_found_condition is not None:
                    if py_trees.blackboard.Blackboard.get("object_found") != object_found_condition:
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        chat_msg={
                            "role": "function",
                            "tool_call_id": self.functions_queue[0].id,
                            "name": self.functions_queue[0].function.name,
                            "content":"[INFO]: The following function was not called due to object_found not being "+str(object_found_condition)+".",
                            }
                        conversation.append(chat_msg)
                        self.functions_queue.pop(0)
                        if len(self.functions_queue) == 0:
                            self.logger.info("No more functions")
                            self.first_run = True
                            py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                            py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                            conversation[-1]["content"] += "This was the last function to call. Please generate a message to the user with feedback on how the execution of all functions went."
                            # conversation[-1].update({"content":updated_content})
                            

                        #self.logger.info("Condition false, function not called")
                        conversation[-1]["content"] += "The system will move on to the next function and try to execute that now."
                        # conversation[-1].update({"content":updated_content})
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
                        py_trees.blackboard.Blackboard.set("STT_flag", False)
                        self.logger.info("Behavior Handler Return: SUCCESS -> object_found_condition")
                        return py_trees.common.Status.SUCCESS # should it be success?
                if current_location_condition is not None:
                    if py_trees.blackboard.Blackboard.get("current_location") != current_location_condition:
                
                        conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                        chat_msg={
                            "role": "function",
                            "tool_call_id": self.functions_queue[0].id,
                            "name": self.functions_queue[0].function.name,
                            "content":"[INFO]: The following function was not called due to current_location not being "+str(current_location_condition)+".",
                            }
                        conversation.append(chat_msg)
                        
                        self.functions_queue.pop(0)
                        if len(self.functions_queue) == 0:
                            self.logger.info("No more functions")
                            self.first_run = True
                            py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                            py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                            conversation[-1]["content"] += "This was the last function to call. Please generate a message to the user with feedback on how the execution of all functions went."
                        self.logger.info("Condition false, function not called due to an location requirement condition not being fulfilled")
                        conversation[-1]["content"] += "The system will move on to the next function and try to execute that now."
                        py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
                        py_trees.blackboard.Blackboard.set("STT_flag", False)
                        self.logger.info("Behavior Handler Return: SUCCESS -> location_condition")
                        return py_trees.common.Status.SUCCESS # should it be success?
                
                # try:
                #     condition_names=args["condition_name"] # Take into consideration that it is a list
                #     condition_values=args["condition_value"]
                # except: 
                #     condition_names=None
                #     condition_values=None
                # self.logger.info("Condition name: %s, Condition value: %s", condition_names, condition_values)
                # if condition_names is not None and condition_values is not None:
                    
                    # for i in range(len(condition_names)):
                    # self.logger.info("Blackboard: ", py_trees.blackboard.Blackboard.get(condition_names[i]))
                    # if py_trees.blackboard.Blackboard.get(condition_names[i]) != condition_values[i]:
                    # if py_trees.blackboard.Blackboard.get(condition_names) != condition_values:
                    #     self.functions_queue.pop(0)
                    #     self.logger.info("Condition false, function not called")
                    #     return py_trees.common.Status.RUNNING # should it be success?
                
                # add what to do if only one of them is not none
                msg = py_trees.blackboard.Blackboard.get("chatgpt/msg")
                if msg:
                    self.logger.info("Behavior Handler: msg for a function")
                    # self.logger.info("Message is provided for the function call")
                    py_trees.blackboard.Blackboard.set("ChatGPT_behavior_msg", True)

                self.logger.info("Following function is being enabled: %s",str(self.functions_queue[0].function.name)+"_behavior")
                #self.logger.info("Function enabled has following id: %s", self.functions_queue[0].id)
                py_trees.blackboard.Blackboard.set(str(self.functions_queue[0].function.name+"_behavior"), "enabled")
                py_trees.blackboard.Blackboard.set("function_id", self.functions_queue[0].id)
                # self.logger.info("TEXT: %s",self.functions_queue[0])
                
                py_trees.blackboard.Blackboard.set("chatgpt/function_call", [self.functions_queue[0]])
                #self.logger.info("Condition True, function called.")
                self.logger.info("funtion call: %s", self.functions_queue[0])
                self.functions_queue.pop(0)
                py_trees.blackboard.Blackboard.set("STT_flag", False)
                return py_trees.common.Status.SUCCESS
            
            elif len(self.functions_queue) == 0:
                self.logger.info("No more functions")
                self.first_run = True
                py_trees.blackboard.Blackboard.set("first_run", self.first_run)
                py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
                conversation = py_trees.blackboard.Blackboard.get("ChatGPT_Conversation")
                conversation[-1]["content"] +=  "Please generate a message to the user with an update on the execution results of all called functions"
                py_trees.blackboard.Blackboard.set("ChatGPT_Conversation", conversation)
                # All function have completed, return to ChatGPT
                # Make sure ALL the behavior functions, when done append a msg with their status.
                # Make sure ALL the behavior functions, check if "ChatGPT_behavior_msg" is true as they then have to speak that instead of the original one.
                py_trees.blackboard.Blackboard.set("STT_flag", False)
                self.logger.info("Behavior Handler Return: FAILURE -> no more function")
                return py_trees.common.Status.FAILURE
                      
        except Exception as e:
            self.logger.error("No behavior enabled because of exception: %s", e)
            py_trees.blackboard.Blackboard.set("STT_flag", True)
            py_trees.blackboard.Blackboard.set("spot_waiting_for_command", True)
            # py_trees.blackboard.Blackboard.set("first_run", False)
            py_trees.blackboard.Blackboard.set("ChatGPT_active", True)
            py_trees.blackboard.Blackboard.set("Result", "ERROR")
        
        #return py_trees.common.Status.FAILURE
        self.logger.info("Behavior Handler Return: SUCCESS")
        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status: py_trees.common.Status) -> None:
        return super().terminate(new_status)
    