from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)

from werkzeug.utils import secure_filename
from config import Config

import os
import traceback

app = Flask(__name__)
app.config.from_object(Config)

# Create uploads folder
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ==========================================
# Home
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# View Uploaded PDF
# ==========================================

@app.route("/pdf/<filename>")
def view_pdf(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==========================================
# Upload PDF (Debug Version)
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    print("\n==============================")
    print("UPLOAD REQUEST RECEIVED")
    print("==============================")

    try:

        if "file" not in request.files:
            print("ERROR: No file received")
            return jsonify({
                "error": "No file uploaded."
            }), 400

        file = request.files["file"]

        if file.filename == "":
            print("ERROR: Empty filename")
            return jsonify({
                "error": "No file selected."
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        print("Saving PDF to:")
        print(filepath)

        file.save(filepath)

        print("PDF saved successfully!")

        if not os.path.exists(filepath):
            print("ERROR: File was not saved.")
            return jsonify({
                "error": "Failed to save file."
            }), 500

        file_size = os.path.getsize(filepath)

        print(f"Saved file size: {file_size} bytes")

        print("Returning success response...")

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully.",
            "filename": filename,
            "pdf_url": f"/pdf/{filename}",
            "size": file_size
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        traceback.print_exc()
        print("===========================\n")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# Ask Question
# ==========================================

@app.route("/ask", methods=["POST"])
def ask():
    return jsonify({
        "message": "Ask endpoint temporarily disabled while debugging."
    })


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)