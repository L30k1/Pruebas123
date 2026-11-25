import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

items = [
    {"id": 1, "name": "Tarea inicial"}
]

@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/<path:filename>")
def static_files(filename):
    if filename.startswith("api/"):
        return jsonify({"error": "Not found"}), 404
    file_path = FRONTEND_DIR / filename
    if file_path.is_file():
        return send_from_directory(FRONTEND_DIR, filename)
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/api/items")
def get_items():
    return jsonify(items), 200

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400

    new_item = {"id": len(items) + 1, "name": name}
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)