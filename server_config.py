import os


def serverSettings():

    if (os.getenv("ENVIRONMENT") is None):
        print("$ENVIRONMENT is not defined, defaulting to dev values.")
        server_config = {'server_binding': '0.0.0.0', 'debug_mode': True}

    elif (os.getenv("ENVIRONMENT") == "production"):
        server_config = {'server_binding': '0.0.0.0', 'debug_mode': False}

    else:
        server_config = {'server_binding': '127.0.0.1', 'debug_mode': True}

    return server_config
