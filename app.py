import os
import json
from flask import Flask, request, jsonify, send_file
from datetime import datetime

app = Flask(__name__)

DB_FILE = "data.json"

# Initialize DB
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"waitlist": [], "survey": []}, f)


def read_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def home():
    return "Backend is running"


# Waitlist endpoint
@app.route("/waitlist", methods=["POST"])
def waitlist():
    data = read_db()

    entry = request.json
    entry["createdAt"] = datetime.utcnow().isoformat()

    data["waitlist"].append(entry)
    write_db(data)

    return jsonify({"success": True})


# Survey endpoint
@app.route("/survey", methods=["POST"])
def survey():
    data = read_db()

    entry = request.json
    entry["createdAt"] = datetime.utcnow().isoformat()

    data["survey"].append(entry)
    write_db(data)

    return jsonify({"success": True})


# Admin download endpoint
@app.route("/admin/data")
def download_data():
    key = request.args.get("key")

    if key != os.environ.get("ADMIN_KEY"):
        return jsonify({"error": "Unauthorized"}), 403

    return send_file(DB_FILE, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
