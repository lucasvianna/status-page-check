import requests
from bs4 import BeautifulSoup


async def status(url):
    code = requests.get(url)
    page = BeautifulSoup(code.text, "html.parser")
    service_status = {}

    for link in page.findAll('tr'):
        service_name = link.find('td', {'class': 'product-name'})
        product_days = link.findAll(
            'td', {'class': 'product-day'})

        if not product_days:
            continue

        status_msg = product_days[-1].find(
            'a', {'class': 'status-icon'})

        if service_name and status_msg:
            service_status[service_name.string.strip()] = status_msg.get("class")[
                1]

    return service_status
