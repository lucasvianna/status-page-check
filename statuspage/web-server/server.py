from flask import Flask
import subprocess
import serverconf

app = Flask(__name__)

@app.route("/")
def index():
    foo = subprocess.call("python3 status-page-check.py", shell=True)
    return(foo)

if __name__ == "__main__":
    app.run(host=serverconf.serverSettings, debug=True, port=5000)
