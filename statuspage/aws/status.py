import requests
from bs4 import BeautifulSoup


def status(url):
    code = requests.get(url)
    page = BeautifulSoup(code.text, "html.parser")
    service_status = {}

    north_america_status = page.find('div', {'id': 'NA_block'})

    for link in north_america_status.findAll('tr'):
        service_name = link.find('td', {'class': 'bb top pad8'})
        service_msg = link.find('td', {'class': 'bb pad8'})

        if service_name and service_msg:
            service_status[service_name.string.strip()
                           ] = service_msg.string.strip()

    return service_status
