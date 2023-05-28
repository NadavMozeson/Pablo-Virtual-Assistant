import json


def load_config():
    with open('config.json') as f:
        config = json.load(f)
        f.close()
        return config

def update_config(key, value):
    data = load_config()
    data[key] = value
    with open('config.json', 'w') as file:
        json.dump(data, file)
        file.close()
