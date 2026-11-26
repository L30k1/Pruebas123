import os
from functools import wraps
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
clerk_client = Clerk(bearer_auth=os.environ.get("CLERK_SECRET_KEY"))
AUTHORIZED_PARTIES = [os.environ.get("AUTHORIZED_PARTIES", "https://pruebas123-2wx0.onrender.com")]

items = [{"id": 1, "name": "Tarea inicial"}]

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request_state = authenticate_request(
            request,
            AuthenticateRequestOptions(authorized_parties=AUTHORIZED_PARTIES)
        )
        if not request_state.is_signed_in:
            return jsonify({"error": "No autorizado", "reason": str(request_state.reason)}), 401
        request.user_id = request_state.payload.get("sub")
        return f(*args, **kwargs)
    return decorated

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
@require_auth
def get_items():
    return jsonify(items), 200

@app.post("/api/items")
@require_auth
def create_item():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400
    new_item = {"id": len(items) + 1, "name": name, "user_id": request.user_id}
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)