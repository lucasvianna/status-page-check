import os

def serverSettings():

    if (os.getenv("ENVIRONMENT") is None):
        print("$ENVIRONMENT is not defined, defaulting to dev values.")
        server_config = {'server_binding': '127.0.0.1'}

    elif (os.getenv("ENVIRONMENT") == "production"):
        server_config = {'server_binding': '0.0.0.0'}

    else:
        server_config = {'server_binding': '127.0.0.1'}

    return server_config

