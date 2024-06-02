import json

TOOLS = [{
        "type": "function",
        "function": {
            "name": "place_probes",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "number_of_probes": {
                        "type": "integer",
                        "description":"The number of probes to place in the fridge"
                    }
                     
                },
                "required": ["computer_brand"],
            },
        }
    }
    ]
