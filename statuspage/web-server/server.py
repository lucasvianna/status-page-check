from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    foo = subprocess.call("python3 status-page-check.py", shell=True)
    return(foo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
