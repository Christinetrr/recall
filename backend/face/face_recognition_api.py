#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List

from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from pyngrok import ngrok, conf
import face_recognition
import numpy as np

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB uploads
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# ----- Globals -----
known_face_encodings: List[np.ndarray] = []
known_face_names: List[str] = []

PROFILES_DIR = Path(__file__).parent / "profiles"

def log(msg: str):
    print(f"[server] {msg}", flush=True)

def load_profiles():
    """Load all profile images. Supports either:
       profiles/Alice.jpg, Bob.png
       or per-person folders: profiles/Alice/*.jpg
    """
    known_face_encodings.clear()
    known_face_names.clear()

    if not PROFILES_DIR.exists():
        log(f"WARNING: Profiles directory not found at {PROFILES_DIR}")
        return

    exts = {".jpg", ".jpeg", ".png", ".bmp"}

    # Case 1: subfolders per person
    has_subdirs = any(p.is_dir() for p in PROFILES_DIR.iterdir())
    if has_subdirs:
        for person_dir in sorted(p for p in PROFILES_DIR.iterdir() if p.is_dir()):
            name = person_dir.name
            for img_path in person_dir.rglob("*"):
                if img_path.suffix.lower() in exts:
                    try:
                        img = face_recognition.load_image_file(str(img_path))
                        encs = face_recognition.face_encodings(img)
                        if encs:
                            known_face_encodings.append(encs[0])
                            known_face_names.append(name)
                            log(f"Loaded {name}: {img_path.name}")
                        else:
                            log(f"SKIP (no face): {img_path}")
                    except Exception as e:
                        log(f"ERROR {img_path}: {e}")
    else:
        # Case 2: flat files named Alice.jpg, Bob.png
        for img_path in sorted(PROFILES_DIR.iterdir()):
            if img_path.suffix.lower() in exts:
                try:
                    img = face_recognition.load_image_file(str(img_path))
                    encs = face_recognition.face_encodings(img)
                    if encs:
                        known_face_encodings.append(encs[0])
                        known_face_names.append(img_path.stem)
                        log(f"Loaded {img_path.stem}")
                    else:
                        log(f"SKIP (no face): {img_path.name}")
                except Exception as e:
                    log(f"ERROR {img_path.name}: {e}")

    log(f"Loaded {len(known_face_names)} profiles: {sorted(set(known_face_names))}")

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "profiles_loaded": len(known_face_names),
        "profiles": sorted(set(known_face_names)),
    })

@app.post("/recognize")
def recognize_face():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided (field name 'image')"}), 400

    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    try:
        img = face_recognition.load_image_file(file)
        boxes = face_recognition.face_locations(img, model="hog")  # 'cnn' if you have GPU
        if not boxes:
            return jsonify({"success": False, "message": "No face detected"}), 404

        if not known_face_encodings:
            return jsonify({"error": "No profiles loaded"}), 500

        encs = face_recognition.face_encodings(img, boxes)
        results = []
        for enc in encs:
            dists = face_recognition.face_distance(known_face_encodings, enc)
            if len(dists) == 0:
                continue
            i = int(np.argmin(dists))
            # Treat < 0.45 as a confident match (tune as needed)
            if dists[i] < 0.45:
                results.append({
                    "name": known_face_names[i],
                    "confidence": float(max(0.0, 1.0 - dists[i])),
                })

        if results:
            best = max(results, key=lambda r: r["confidence"])
            return jsonify({"success": True, **best})
        return jsonify({"success": False, "message": "No matching profile"}), 404

    except Exception as e:
        return jsonify({"error": f"Processing error: {e}"}), 500

def start_ngrok(port: int) -> str:
    # Prefer env var token if set; otherwise use default ngrok config.
    token = os.environ.get("NGROK_AUTHTOKEN")
    if token:
        conf.get_default().auth_token = token
        log("ngrok auth token set from $NGROK_AUTHTOKEN")

    # Create HTTP tunnel and return https URL
    tunnel = ngrok.connect(addr=port, proto="http", bind_tls=True)
    public_url = tunnel.public_url
    log(f"ngrok tunnel online: {public_url}")
    return public_url

def main():
    print("=" * 60)
    print("Face Recognition API (Flask + ngrok)")
    print("=" * 60)

    log("Loading profiles...")
    load_profiles()
    if not known_face_names:
        log(f"NOTE: add images under {PROFILES_DIR} (flat or per-person folders)")

    port = int(os.environ.get("PORT", "5000"))
    public_url = start_ngrok(port)

    print("\n" + "=" * 60)
    print(f"🌐 Public URL: {public_url}")
    print("=" * 60)
    print("Endpoints:")
    print(f"  GET  {public_url}/health")
    print(f"  POST {public_url}/recognize   (multipart form, field 'image')")
    print("\nExample:")
    print(f"""  curl -X POST \\
    -F "image=@/absolute/path/to/image.jpg" \\
    {public_url}/recognize
""")

    # IMPORTANT: bind to 0.0.0.0 and disable reloader
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
