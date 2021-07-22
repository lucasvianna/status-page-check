from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    foo = subprocess.getoutput("python3 status_page_check.py --failed")
    return(foo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
