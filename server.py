from flask import Flask
from flask import request
import subprocess
import serverconfig
import status_page_check as sp

app = Flask(__name__)


@app.route("/")
def index():
    results = sp.web_version()
    return(results)


@app.route("/page")
def filtered_results():
    page_name = request.args.get('page')
    search_svc_filter = request.args.get('filter')
    show_failed_only = request.args.get('failed_only')

    results = sp.web_version(page_name)
    return(results)


if __name__ == "__main__":
    config = serverconfig.serverSettings()
    app.run(host=config["server_binding"],
            debug=config["debug_mode"], port=5000)
