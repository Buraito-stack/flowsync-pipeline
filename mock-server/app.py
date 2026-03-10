import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "customers.json")


def load_customers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "mock-server"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
