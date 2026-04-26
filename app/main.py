from flask import Flask, jsonify, request, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.path.join("data", "sensor_data.json")


def load_sensor_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_sensor_data(data):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route("/")
def home():
    data = load_sensor_data()
    latest = data[-1] if data else None
    return jsonify({
        "message": "Smart Farm Server Running",
        "latest": latest
    })


@app.route("/api/sensor", methods=["GET"])
def get_sensor_data():
    data = load_sensor_data()
    return jsonify(data)


@app.route("/api/sensor", methods=["POST"])
def receive_sensor_data():
    new_data = request.get_json()

    if not new_data:
        return jsonify({"error": "No JSON received"}), 400

    new_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = load_sensor_data()
    data.append(new_data)
    save_sensor_data(data)

    return jsonify({
        "message": "Data received",
        "data": new_data
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)