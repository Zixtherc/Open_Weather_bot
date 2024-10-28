import os
import json

def load_json(name_json : str, value_file : str):
    path = os.path.abspath(__file__ + f'../../../static/{name_json}')
    
    with open (file = path, mode = "w") as file:
        json.dump(
            obj = value_file,
            ensure_ascii = False,
            indent = 4,
            fp = file
        )