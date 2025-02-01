from os.path import abspath, join
import json

def read_json (name_json : str):
    try:

        path = abspath(join(__file__, '..', '..', 'static', name_json))
        print(path)

        with open(path, "r") as file: 
            return json.load(file)
    except Exception as error:
        print(f'Возможно вы забыли добавить .json к name_json, проверь всё заново пожалуйста ')