import requests
import json
from bs4 import BeautifulSoup


async def status(url):
    code = requests.get(url)
    service_status = {}

    components = json.loads(code.text)

    for component in components["components"]:
        service_name = component["name"]
        service_msg = component["status"]

        if service_name and service_msg:
            service_status[service_name.strip()
                           ] = service_msg.strip()

    return service_status
