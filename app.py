#!/usr/bin/env python3
"""
Markdowner Web App
A browser-based tool to convert files to Markdown using Microsoft's markitdown.
Upload files via drag & drop, preview the Markdown, and download the results.
"""

import io
import os
import tempfile
import zipfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from markitdown import MarkItDown
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB total upload limit

converter = MarkItDown()


@app.route("/")
def index():
    """Serve the single-page UI."""
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    """Convert one or more uploaded files to Markdown.

    Returns JSON: { results: [{ name, markdown, error }] }
    """
    uploaded = request.files.getlist("files")
    if not uploaded:
        return jsonify({"error": "No files uploaded."}), 400

    results = []
    for file_storage in uploaded:
        original_name = file_storage.filename or "file"
        safe_name = secure_filename(original_name) or "file"
        suffix = Path(safe_name).suffix

        # markitdown needs a real file path; write to a temp file first.
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix
            ) as tmp:
                file_storage.save(tmp.name)
                tmp_path = tmp.name

            result = converter.convert(tmp_path)

            results.append(
                {
                    "name": Path(original_name).stem + ".md",
                    "markdown": result.text_content,
                    "error": None,
                }
            )
        except Exception as e:  # noqa: BLE001 - surface any conversion error to UI
            results.append(
                {"name": original_name, "markdown": None, "error": str(e)}
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    return jsonify({"results": results})


@app.route("/download-zip", methods=["POST"])
def download_zip():
    """Bundle multiple converted Markdown files into a single .zip download."""
    data = request.get_json(silent=True) or {}
    files = data.get("files", [])
    if not files:
        return jsonify({"error": "No files to bundle."}), 400

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in files:
            name = secure_filename(item.get("name", "file.md")) or "file.md"
            zf.writestr(name, item.get("markdown", ""))
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="markdown-files.zip",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
