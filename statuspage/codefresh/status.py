import requests
from bs4 import BeautifulSoup


def status(url):
    code = requests.get(url)
    page = BeautifulSoup(code.text, "html.parser")
    service_status = {}

    for link in page.findAll('div', {'class': 'component-container'}):
        service_name = link.find('span', {'class': 'name'})
        service_msg = link.find('span', {'class': 'component-status'})

        if service_name and service_msg:
            service_status[service_name.string.strip()
                           ] = service_msg.string.strip()

    return service_status
