import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "customers.json")


def load_customers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "mock-server"})


@app.route("/api/customers", methods=["GET"])
def get_customers():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if page < 1:
        page = 1
    if limit < 1 or limit > 100:
        limit = 10

    customers = load_customers()
    total = len(customers)

    start = (page - 1) * limit
    end = start + limit
    paginated = customers[start:end]

    return jsonify({
        "data": paginated,
        "total": total,
        "page": page,
        "limit": limit
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
