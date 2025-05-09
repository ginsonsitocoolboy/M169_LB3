from flask import Flask, request, jsonify, send_from_directory
from docker_manager import create_server, start_server, stop_server, delete_server, list_servers

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/servers")
def servers():
    return jsonify(list_servers())

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    return jsonify(create_server(data["name"]))

@app.route("/start/<name>", methods=["POST"])
def start(name):
    return jsonify(start_server(name))

@app.route("/stop/<name>", methods=["POST"])
def stop(name):
    return jsonify(stop_server(name))

@app.route("/delete/<name>", methods=["POST"])
def delete(name):
    return jsonify(delete_server(name))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
