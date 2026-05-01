from flask import Blueprint, render_template
import json
import os

dashboard_bp = Blueprint("dashboard", __name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(_BASE_DIR, "..", "data", "sensor_data.json")


def _load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@dashboard_bp.route("/dashboard")
def dashboard():
    data = _load_data()
    latest = data[-1] if data else None
    history = list(reversed(data))
    return render_template("index.html", latest=latest, history=history)
