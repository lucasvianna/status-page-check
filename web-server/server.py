from flask import Flask
import subprocess
import serverconf
import status_page_check as sp

app = Flask(__name__)

@app.route("/")
def index():
    results = sp.web_version()
    return(results)

if __name__ == "__main__":
    app.run(host=serverconf.serverSettings, debug=True, port=5000)
