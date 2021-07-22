from flask import Flask
import subprocess
import serverconfig
import status_page_check as sp

app = Flask(__name__)

@app.route("/")
def index():
    results = sp.web_version()
    return(results)

if __name__ == "__main__":
    config = serverconfig.serverSettings()
    app.run(host=config["server_binding"], debug=config["debug_mode"], port=5000)
