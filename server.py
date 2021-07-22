from flask import Flask
import subprocess
import status_page_check as sp

app = Flask(__name__)


@app.route("/")
def index():
    results = sp.web_version()
    return(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
