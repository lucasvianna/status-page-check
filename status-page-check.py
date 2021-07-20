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
    # TODO: paralyze it
    load_config()
    service_status = {}
    for page in settings["pages"]:
        if settings["pages"][page]["enable"]:
            page_url = settings["pages"][page]["url"]
            module_name = "statuspage." + page + ".status"
            module = importlib.import_module(module_name)
            service_status[page] = module.status(page_url)

    print(json.dumps(service_status, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
