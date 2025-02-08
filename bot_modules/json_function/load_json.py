from os.path import abspath, join
import json

def load_json(name_json : str, value_file : str):
    path = abspath(join(__file__, '..', '..', '..', 'static', name_json))
    
    with open (file = path, mode = "w", encoding = "utf-8") as file:
        json.dump(
            obj = value_file,
            ensure_ascii = False,
            indent = 4,
            fp = file
        )