from flask import Flask
from flask import request, render_template

import subprocess
import server_config
import status_page_check as sp

app = Flask(__name__)


def status_background_style(status):
    status_style = "none"
    severity = {x.lower(): k for k,
                v in sp.settings["status"].items() for x in v}

    if status.lower() in severity.keys():
        status_style = severity[status.lower()]

    if status_style == "error":
        status_style = "danger"
    return status_style


@app.route("/")
def index():
    page_name = request.args.get('page')
    search_svc_filter = request.args.get('filter')
    show_failed_only = request.args.get('failed_only')

    results = sp.web_version(
        page=page_name, search_svc_filter=search_svc_filter, show_failed_only=show_failed_only)

    return render_template('index.html', results=results, status_background_style=status_background_style)
    # return(results)


if __name__ == "__main__":
    config = server_config.serverSettings()
    app.run(host=config["server_binding"],
            debug=config["debug_mode"], port=5000)
