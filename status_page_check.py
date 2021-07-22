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
show_failed_services = False
show_summary = False
filtered_page = None  # filtered page
search_filter = None


def load_config():
    global settings
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as stream:
            try:
                settings = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)


def set_options():
    global parser, show_failed_services, show_summary, filtered_page, search_filter
    parser.add_argument("--page", help="")
    parser.add_argument(
        "--failed", help="show failed services", action="store_true")
    parser.add_argument(
        "--summary", help="show the summary per page", action="store_true")
    parser.add_argument("--filter", help="Filter services")
    args = parser.parse_args()

    if args.failed:
        show_failed_services = True
    if args.summary:
        show_summary = True
    if args.page:
        filtered_page = args.page.strip()
    if args.filter:
        search_filter = args.filter


def find_color(status):
    color = settings["status_color"]["default"]
    severity = {x.lower(): k for k,
                v in settings["status"].items() for x in v}

    if status in severity.keys():
        if severity[status]:
            color = settings["status_color"][severity[status]]

    return color


def process_results():
    # {"page": {ok: 10, error: 2, warn: 1, services: {svc_name: name, svc_status: status}}}
    global service_status
    compiled_svc_status = {}

    for page, svc_statuses in service_status.items():
        compiled_svc_status[page] = {"error": 0, "warn": 0, "ok": 0}
        for svc, svc_status in svc_statuses.items():
            if svc_status.lower() in settings["status"]["ok"]:
                compiled_svc_status[page]["ok"] += 1
            if svc_status.lower() in settings["status"]["warn"]:
                compiled_svc_status[page]["warn"] += 1
            if svc_status.lower() in settings["status"]["error"]:
                compiled_svc_status[page]["error"] += 1
        compiled_svc_status[page]["services"] = svc_statuses
    return compiled_svc_status


def print_summary(results, failed_only=False, filtered_page=None):
    print("\nSummary:")

    if failed_only:
        results = dict(filter(
            lambda elem: elem[1]["warn"] > 0 or elem[1]["error"] > 0, results.items()))

    for page, svc_data in results.items():
        if filtered_page != None and page.upper() != filtered_page.upper():
            continue

        print_summary_table(
            page.upper(), svc_data["ok"], svc_data["warn"], svc_data["error"])


def print_summary_table(page, svc_ok, svc_warn, svc_error):
    print(colored(page.upper(), 'white').ljust(20),
          colored(svc_ok,
                  settings["status_color"]["ok"]).ljust(20),
          colored(svc_warn,
                  settings["status_color"]["warn"]).ljust(20),
          colored(svc_error,
                  settings["status_color"]["error"]))


def print_list(results, failed_only=False, filtered_page=None, search_filter=None):
    if failed_only:
        # filtes pages with failed services
        results = dict(filter(
            lambda elem: elem[1]["warn"] > 0 or elem[1]["error"] > 0, results.items()))
    if filtered_page:
        results = dict(
            filter(lambda elem: elem[0].upper() == filtered_page.upper(), results.items()))

    for page, svc_data in results.items():
        print(f'\n{colored(page.upper(), "blue")}')
        services_statuses = svc_data["services"]

        # filter services that failed
        if failed_only:
            services_statuses = dict(filter(
                lambda elem: elem[1].lower() not in settings["status"]["ok"], services_statuses.items()))

        if search_filter:
            services_statuses = dict(filter(
                lambda elem: search_filter.lower() in elem[0].lower(), services_statuses.items()))

        for svc_name, svc_status in services_statuses.items():
            color = find_color(svc_status.lower())
            print(colored(svc_name, 'white').ljust(
                80), colored(svc_status, color))


def print_results(results):
    global show_failed_services, show_summary, filtered_page, search_filter

    if show_summary:
        print_summary(results, failed_only=show_failed_services,
                      filtered_page=filtered_page)

    else:
        print_list(results, failed_only=show_failed_services, filtered_page=filtered_page,
                   search_filter=search_filter)


async def read_pages():
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


def main():
    asyncio.run(read_pages())
    results = process_results()
    print_results(results)


def web_version():
    load_config()
    asyncio.run(read_pages())
    results = process_results()
    return json.dumps(results, indent=4, sort_keys=True)


if __name__ == "__main__":
    set_options()
    load_config()
    main()
    # print(json.dumps(results, indent=4, sort_keys=True))
