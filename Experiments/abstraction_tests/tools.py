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
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    },
                    "go_through_areas": {
                        "type": "array",
                        "description": "",
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    },
                    "object_found_condition": {
                        "type": "boolean",
                        "description": "",
                        "enum": [True, False],
                    },
                    "current_location_condition": {
                        "type": "string",
                        "description": "",
                        "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
                    }
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
              "enum": ["banana", "apple", "cup", "laptop", "dog", "cat", "bottle", "teddy bear", "person", "bowl", "refrigerator"]
            },
            "object_found_condition": {
                        "type": "boolean",
                        "description": "",
                        "enum": [True, False],
                    },
            "current_location_condition": {
                "type": "string",
                "description": "",
                "enum": ["kitchen", "office", "bed room", "living room", "dining room", "workshop", "garden", "garage", "home"],
            }
          },
          "required": ["object"]
        }
      }
    }
    ]
