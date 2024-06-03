##### Contains all the tool description avalible to chatGPT #####

##### Quick Guide ####


TOOLS = [{
        "type": "function",
        "function": {
            "name": "go_to_area_behavior",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_area": {
                        "type": "string",
                        "description":"",
                        "enum": ["Kitchen", "Office", "Bed Room", "Living Room", "Dining Room", "Workshop", "Garden", "Garage", "Home"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "",
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
        "description": "",
        "parameters": {
          "type": "object",
          "properties": {
            "object": {
              "type": "string",
              "description": "",
              "enum": ["Banana", "Apple", "Cup", "Laptop", "Dog", "Cat", "Bottle", "Teddy Bear", "Person", "Bowl", "Refrigerator"]
            },
          },
          "required": ["object"]
        }
      }
    }
    ]
