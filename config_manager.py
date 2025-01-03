import json
import os

CONFIG_FILE = 'channels_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def add_channel_group_pair(channel_id, group_id):
    config = load_config()
    config[str(channel_id)] = group_id
    save_config(config)

def get_channel_group_pairs():
    return load_config()