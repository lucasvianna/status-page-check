import requests
from bs4 import BeautifulSoup


def status(url):
    code = requests.get(url)
    page = BeautifulSoup(code.text, "html.parser")
    service_status = {}

    for link in page.findAll('div', {'class': 'status_td'}):
        service_names = link.find('p', {'class': 'component_name'})
        service_msg = link.find('p', {'class': 'component-status'})

        # some status page do not have the correct syntax
        for sa in service_names.stripped_strings:
            service_name = sa.strip()

        if service_name and service_msg:
            service_status[service_name] = service_msg.string.strip()

    return service_status
