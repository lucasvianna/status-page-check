import unittest
import requests
import server_config

server_binding = server_config.serverSettings()["server_binding"]
SERVER_URL = f"http://{server_binding}:5000"


def test_index():
    response = requests.get(SERVER_URL + "/")

    assert response.status_code == 200
