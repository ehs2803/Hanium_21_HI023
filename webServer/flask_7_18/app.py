import socket
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def print_hello():
    while True:
        print(1)
    a=1
    return str(a)

@app.route("/info", methods=["POST"])
def info():
    info_dict = dict()
    info_dict["IP_ADDRESS"] = socket.gethostbyname(socket.gethostname())
    info_dict["HOST_NAME"] = socket.gethostname()
    return info_dict

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
