import json


def get_products():
    with open("./data/products.json", "r") as file:
        data = json.load(file)

    return data
