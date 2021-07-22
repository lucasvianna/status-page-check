import os

def serverSettings():

    if (os.environ("ENVIRONMENT") == "production"):
        server_config = {'server_binding': '0.0.0.0'}
    else:
        server_config = {'server_binding': '127.0.0.1'}

    return server_config
