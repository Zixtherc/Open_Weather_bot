from os.path import abspath, join
import json

def read_json (name_json : str):
    
    path = abspath(join(__file__, '..', '..', 'static', name_json))
    
    with open(path, "r") as file: 
        return json.load(file)