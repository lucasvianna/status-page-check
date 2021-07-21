import argparse
import asyncio
import importlib
import json
import sys
import yaml
from os import path
from termcolor import colored

CONFIG_FILE = "./settings.yaml"
service_status = {}
parser = argparse.ArgumentParser()
failed_services_only = False
summary = False


def load_config():
    global settings
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as stream:
            try:
                settings = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)


def set_options():
    global parser, failed_services_only, summary
    parser.add_argument("--page", help="")
    parser.add_argument(
        "--failed", help="show failed services", action="store_true")
    parser.add_argument(
        "--summary", help="show the summary per page", action="store_true")
    parser.add_argument("--filter", help="Filter services")
    args = parser.parse_args()

    if args.failed:
        failed_services_only = True
    if args.summary:
        summary = True


def find_color(status):
    color = settings["status_color"]["default"]
    severity = {x.lower(): k for k,
                v in settings["status"].items() for x in v}

    if status in severity.keys():
        if severity[status]:
            color = settings["status_color"][severity[status]]

    return color


def print_results(results):
    global failed_services_only

    for svc, services_status in results.items():
        print(f'\n{colored(svc.upper(), "blue")}')

        for svc, svc_status in services_status.items():
            if failed_services_only:
                if svc_status.lower() not in settings["status"]["ok"]:
                    color = find_color(svc_status.lower())
                    print(colored(svc, 'white').ljust(
                        80), colored(svc_status, color))
            else:
                color = find_color(svc_status.lower())
                print(colored(svc, 'white').ljust(
                    80), colored(svc_status, color))


async def main():
    global service_status
    for page in settings["pages"]:
        if settings["pages"][page]["enable"]:
            try:
                page_url = settings["pages"][page]["url"]
                module_name = "statuspage." + page + ".status"
                module = importlib.import_module(module_name)
                print(f"Checking {page.upper()}...")
                service_status[page] = await module.status(page_url)
            except Exception as e:
                print(f"Unable to import {module_name}", e)


if __name__ == "__main__":
    set_options()
    load_config()
    asyncio.run(main())
    print_results(service_status)
