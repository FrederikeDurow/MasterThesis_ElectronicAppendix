##### Contains all the tool description avalible to chatGPT #####

##### Quick Guide ####


TOOLS = [{
        "type": "function",
        "function": {
            "name": "go_to_area_behavior",
            "description": "This function commands the robot to move to a predefined location within the environment, adhering strictly to specified and recognized areas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_area": {
                        "type": "string",
                        "description":"The specific area to which the robot is directed. Acceptable values include: Kitchen, Office, Bed Room, Living Room, Dining Room, Workshop, Garden, Garage, and Home. Any other area will be rejected.",
                        "enum": ["Kitchen", "Office", "Bed Room", "Living Room", "Dining Room", "Workshop", "Garden", "Garage", "Home"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "Optional list of areas for the robot to traverse on its way to the destination. Each area must be from the predefined list, such as Kitchen, Office, etc. Specifying areas not on the list will prompt a request for clarification.",
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
        "description": "This function enables the robot to search for and identify specific objects within its operational range, using its visual recognition capabilities. Only objects from a predefined list are recognized.",
        "parameters": {
          "type": "object",
          "properties": {
            "object": {
              "type": "string",
              "description": "The item the robot is tasked to find. It must be one of the predefined objects: Banana, Apple, Cup, Laptop, Dog, Cat, Bottle, Teddy Bear, Person, Bowl, or Refrigerator. Requests to locate any objects not on this list will be rejected.",
              "enum": ["Banana", "Apple", "Cup", "Laptop", "Dog", "Cat", "Bottle", "Teddy Bear", "Person", "Bowl", "Refrigerator"]
            },
          },
          "required": ["object"]
        }
      }
    }
    ]
