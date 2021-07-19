from os import path
import json
import importlib

CONFIG_FILE = "./settings.json"

def load_config():
    global settings
    if path.exists(CONFIG_FILE):
        json_file = open(CONFIG_FILE,)
        settings = json.load(json_file)
        json_file.close()

def main():
    load_config()
    for page in settings["pages"]:
        page_url = settings["pages"][page]
        module_name = "statuspage." + page
        module = importlib.import_module(module_name)
        module.status(page_url)

if __name__ == "__main__":
    main()
    