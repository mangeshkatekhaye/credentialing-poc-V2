# services/scenario_loader.py

import json
import os


def load_scenario(name):
    """
    Load predefined scenario:
    'complete', 'partial', 'incomplete'
    """

    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "scenarios", f"{name}.json")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    except Exception as e:
        print("Error loading scenario:", e)
        return {}
        
if __name__ == "__main__":
    data = load_scenario("partial")
    print(data)