import os 
import json

def read_json (name_json : str):
    
    path = os.path.abspath(__file__ + f'../../../static/{name_json}')
    
    with open(path, "r") as file: 
        return json.load(file)