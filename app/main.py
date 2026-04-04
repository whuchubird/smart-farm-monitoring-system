from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "sensor_data.json")

def load_sensor_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

@app.route("/")
def home():
    data = load_sensor_data()
    latest = data[-1] if data else None
    return render_template("index.html", latest=latest)

@app.route("/api/sensor")
def get_sensor_data():
    data = load_sensor_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)