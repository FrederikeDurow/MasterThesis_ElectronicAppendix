##### Contains all the tool description avalible to chatGPT #####

##### Quick Guide ####


TOOLS = [{
        "type": "function",
        "function": {
            "name": "go_to_area_behavior",
            "description": "Navigate to a desired location or area through poses.\n Inputs must provided by user and be one from the enum list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_area": {
                        "type": "string",
                        "description":"The goal location \nThis is the area you should end up in.\n This value must be obtained directly from user input, not by AI guessing. The value must be exactly one from the list, otherwise ask the user for valid value. If the user has not stated their preference from the allowed choices in the enum list, the function cannot be used, but instead clarifying questions to user are required.",
                        "enum": ["Kitchen", "Office", "Bed Room", "Living Room", "Dining Room", "Workshop", "Garden", "Garage", "Home"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "Which area should be navigated through before reaching the goal area\n, Will navigate through these area in the order they are added. This value must be obtained directly from user input, not by AI guessing. If the user has not stated their preference from the allowed choices in the enum list, the function cannot be used, but instead clarifying questions to user are required.\n",
                        "enum": ["Kitchen", "Office", "Bed Room", "Living Room", "Dining Room", "Workshop", "Garden", "Garage", "Home"],
                    },
                },
                "required": ["goal_area"],
            },
        }
    },
    {
      "type": "function",
      "function": {
        "name": "locate_object",
        "description": "Start looking for one of the object in the enum list at current location. User most directly request this tool call, not by AI guessing. Ask clarifying question if needed.",
        "parameters": {
          "type": "object",
          "properties": {
            "object": {
              "type": "string",
              "description": "The user most directly request looking for an object. This value must be obtained directly from user input, not by AI guessing. If the user has not stated their preference from the allowed choices, the function cannot be used, but instead clarifying questions to user are required.",
              "enum": ["Banana", "Apple", "Cup", "Laptop", "Dog", "Cat", "Bottle", "Teddy Bear", "Person", "Bowl", "Refrigerator"]
            },
          },
          "required": ["object"]
        }
      }
    }
    ]
