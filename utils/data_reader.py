import json


def read_json(path):
    with open(path, "r") as file:
        data = json.load(file)

    return data
