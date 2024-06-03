##### Contains all the tool description avalible to chatGPT #####

##### Quick Guide ####


TOOLS = [{
        "type": "function",
        "function": {
            "name": "go_to_area",
            "description": "Navigate to a desired location or area through poses.\n Inputs must provided by user and be one from the enum list. ",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_area": {
                        "type": "string",
                        "description":"The goal location",
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "Which area should be navigated through before reaching the goal area\n",
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    },
                    "object_found_condition": {
                        "type": "boolean",
                        "description": "This is an optional parameter, only set for functions that have a condition. If set, the function is only called if the object_found parameter is equal to the set value (true or false).",
                        "enum": [True, False],
                    },
                    "current_location_condition": {
                        "type": "string",
                        "description": "This is an optional parameter, only set for functions that have a condition. If set, the function is only called if the current_location parameter is equal to the set value from the enum list.",
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    }
                    
                    # "condition_name": {
                    #     "type": "array",
                    #     "description": "The name of the condition(s) that decides whether the function should be executed or not. The condition_name and condition_value belong together, either both of them have to be set or none of them.",
                    #     "enum": ["current_location", "object_found"],
                    # },
                    # "condition_value": {
                    #     "type": "array",
                    #     "description": "The value of the condition(s) that decides whether the function should be executed or not. The condition_name and condition_value belong together, either both of them have to be set or none of them.",
                    #     "enum": [True, False ,"office","kitchen","home"],
                    # }
                      
                },
                "required": ["goal_area"],
            },
        }
    },
    {
      "type": "function",
      "function": {
        "name": "locate_object",
        "description": "Start looking for the input object",
        "parameters": {
          "type": "object",
          "properties": {
            "object": {
              "type": "string",
              "description": "The user most directly request looking for an object.",
              "enum": ["banana", "apple", "cup", "laptop", "dog", "cat", "bottle", "teddy bear", "person", "bowl", "refrigerator"]
            },
            "object_found_condition": {
                "type": "boolean",
                "description": "This is an optional parameter, only set for functions that have a condition. If set, the function is only called if the object_found parameter is equal to the set value (true or false).",
                "enum": [True, False],
            },
            "current_location_condition": {
                "type": "string",
                "description": "This is an optional parameter, only set for functions that have a condition. If set, the function is only called if the current_location parameter is equal to the set value from the enum list.",
                "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
            }
            # "condition_name": {
            #     "type": "array",
            #     "description": "The name of the condition(s) that decides whether the function should be executed or not. The condition_name and condition_value belong together, either both of them have to be set or none of them.",
            #     "enum": ["current_location", "object_found"],
            # },
            # "condition_value": {
            #     "type": "array",
            #     "description": "The value of the condition(s) that decides whether the function should be executed or not. The condition_name and condition_value belong together, either both of them have to be set or none of them.",
            #     "enum": [True, False ,"office","kitchen","home"],
            # }
          },
          "required": ["object"]
        }
      }
    }
    ]
