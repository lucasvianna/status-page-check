import argparse
import asyncio
import importlib
import json
import sys
import yaml
import redis
from os import path
from termcolor import colored

CONFIG_FILE = "./settings.yaml"
service_status = {}
parser = argparse.ArgumentParser()
show_failed_services = False
show_summary = False
filtered_page = None  # filtered page
search_filter = None
redis_conn = redis.Redis(host='redis')


def cache_exists():
    return redis_conn.exists("status_page_status")


def read_from_cache():
    return json.loads(redis_conn.get("status_page_status"))


def write_cache():
    global service_status
    redis_conn.set("status_page_status", json.dumps(service_status))
    redis_conn.expire("status_page_status", 600)


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
    # {"page": {success: 10, error: 2, warning: 1, services: {svc_name: name, svc_status: status}}}
    global service_status, show_failed_services, filtered_page, search_filter
    results = service_status

    if filtered_page:
        results = dict(
            filter(lambda elem: elem[0].upper() == filtered_page.upper(), results.items()))

    compiled_svc_status = {}

    for page, svc_statuses in results.items():
        compiled_svc_status[page] = {"error": 0, "warning": 0, "success": 0}
        for svc, svc_status in svc_statuses.items():
            if svc_status.lower() in settings["status"]["success"]:
                compiled_svc_status[page]["success"] += 1
            if svc_status.lower() in settings["status"]["warning"]:
                compiled_svc_status[page]["warning"] += 1
            if svc_status.lower() in settings["status"]["error"]:
                compiled_svc_status[page]["error"] += 1

        if search_filter:
            svc_statuses = dict(filter(
                lambda elem: search_filter.lower() in elem[0].lower(), svc_statuses.items()))

        if show_failed_services:
            svc_statuses = dict(filter(
                lambda elem: elem[1].lower() not in settings["status"]["success"], svc_statuses.items()))

        compiled_svc_status[page]["services"] = svc_statuses

    if show_failed_services:
        compiled_svc_status = dict(filter(
            lambda elem: elem[1]["warning"] > 0 or elem[1]["error"] > 0, compiled_svc_status.items()))

    return compiled_svc_status


def print_summary(results, failed_only=False, filtered_page=None):
    print("\nSummary:")

    for page, svc_data in results.items():
        if filtered_page != None and page.upper() != filtered_page.upper():
            continue

        print_summary_table(
            page.upper(), svc_data["success"], svc_data["warning"], svc_data["error"])


def print_summary_table(page, svc_success, svc_warning, svc_error):
    print(colored(page.upper(), 'white').ljust(20),
          colored(svc_success,
                  settings["status_color"]["success"]).ljust(20),
          colored(svc_warning,
                  settings["status_color"]["warning"]).ljust(20),
          colored(svc_error,
                  settings["status_color"]["error"]))


def print_list(results):
    print(json.dumps(results, indent=4, sort_keys=True))
    for page, svc_data in results.items():
        print(f'\n{colored(page.upper(), "blue")}')
        services_statuses = svc_data["services"]

        for svc_name, svc_status in services_statuses.items():
            color = find_color(svc_status.lower())
            print(colored(svc_name, 'white').ljust(
                80), colored(svc_status, color))


def print_results(results):
    global show_summary

    if show_summary:
        print_summary(results)
    else:
        print_list(results)


async def read_pages():
    global service_status
    if cache_exists():
        service_status = read_from_cache()
    else:
        for page in settings["pages"]:
            if settings["pages"][page]["enable"]:
                try:
                    page_url = settings["pages"][page]["url"]
                    module_name = "statuspage." + page + ".status"
                    module = importlib.import_module(module_name)
                    service_status[page] = await module.status(page_url)
                except Exception as e:
                    print(f"Unable to import {module_name}", e)
        write_cache()


def main():
    asyncio.run(read_pages())
    results = process_results()
    print_results(results)


def web_version(page=None, search_svc_filter=None, show_failed_only=False):
    global filtered_page, show_failed_services, search_filter
    filtered_page = page
    show_failed_services = show_failed_only
    search_filter = search_svc_filter

    load_config()
    asyncio.run(read_pages())
    results = process_results()
    # return(json.dumps(results, indent=4, sort_keys=True))
    return results


if __name__ == "__main__":
    set_options()
    load_config()
    main()
    # print(json.dumps(results, indent=4, sort_keys=True))
