from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from app.scan_upload import scan_html_text
from app.scoring import is_wcag, score

ROOT = Path(__file__).resolve().parent.parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB


@app.get("/")
def index():
    return send_from_directory(ROOT / "web", "index.html")


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="File is too large (limit 2 MB)."), 413


@app.post("/api/scan")
def scan():
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        return jsonify(error="No file uploaded."), 400
    if not upload.filename.lower().endswith((".html", ".htm")):
        return jsonify(error="Only .html or .htm files are supported right now."), 400
    try:
        html = upload.read().decode("utf-8")
    except UnicodeDecodeError:
        return jsonify(error="File must be UTF-8 text."), 400

    result = scan_html_text(html)
    scored = [v for v in result["violations"] if is_wcag(v)]
    advice = [v for v in result["violations"] if not is_wcag(v)]
    return jsonify(
        filename=upload.filename,
        score=score(scored),
        violations=scored,
        advice=advice,
        incomplete=result["incomplete"],
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
