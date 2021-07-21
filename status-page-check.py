from os import path
import yaml
import json
import importlib
from termcolor import colored

CONFIG_FILE = "./settings.yaml"


def load_config():
    global settings
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as stream:
            try:
                settings = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)


def find_color(status):
    default_color = "white"
    colors = {x.lower(): k for k,
              v in settings["status_color"].items() for x in v}

    color = colors[status] if status in colors.keys() else default_color
    return color


def print_results(page, services):
    print(colored(page.upper(), "blue"))
    for svc, svc_status in services.items():
        color = find_color(svc_status.lower())
        print(colored(svc, 'white'), colored(svc_status, color))


def main():
    load_config()
    service_status = {}
    for page in settings["pages"]:
        if settings["pages"][page]["enable"]:
            page_url = settings["pages"][page]["url"]
            module_name = "statuspage." + page + ".status"
            module = importlib.import_module(module_name)
            service_status[page] = module.status(page_url)
            print_results(page, service_status[page])

    # print(json.dumps(service_status, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
