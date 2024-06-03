##### Contains all the tool description avalible to chatGPT #####

##### Quick Guide ####


TOOLS = [{
        "type": "function",
        "function": {
            "name": "go_to_area_behavior",
            "description": "Navigate to a desired location",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_area": {
                        "type": "string",
                        "description":"The goal location",
                        "enum": ["kitchen", "office", "bedroom", "living room", "dining room", "workshop", "garden", "garage", "ome"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "Which area should be navigated through before reaching the goal area",
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
        "description": "Start looking for the input object",
        "parameters": {
          "type": "object",
          "properties": {
            "object": {
              "type": "string",
              "description": "The user most directly request looking for an object.",
              "enum": ["Banana", "Apple", "Cup", "Laptop", "Dog", "Cat", "Bottle", "Teddy Bear", "Person", "Bowl", "Refrigerator"]
            },
          },
          "required": ["object"]
        }
      }
    }
    ]
