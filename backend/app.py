import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend en otro puerto/origen

items = [
    {"id": 1, "name": "Tarea inicial"}
]

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