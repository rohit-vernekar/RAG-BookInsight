from typing import Dict

import yaml

file_path = "config.yaml"

try:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        openai_config = config["openai_config"]
        query_config = config["query_config"]
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")
