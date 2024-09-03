import os
import json

from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from model.layoutlmv3 import LayoutLMv3Model
from utils.post_processing import (
    get_entities,
    get_best_entity_by_confidence,
    filter_entities_by_confidence,
    parse_monetary_values,
)

# Configuration variables
UPLOAD_FOLDER = "uploads/"
MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB max file size
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}

# Creating the app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# Model class
model = LayoutLMv3Model()


# Routes
@app.route("/", methods=["GET"])
def upload_form():
    return render_template("upload.html")


# Check if file extension is allowed
def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/process_document", methods=["POST"])
def process_document():
    # Check if the post request has the file part
    if "document" not in request.files:
        return jsonify({"error": "No document part"}), 400

    file = request.files["document"]

    # Check if the file is empty
    if file.filename == "":
        return jsonify({"error": "Empty document"}), 400

    # Check if the file type is allowed
    if not is_allowed_file(file.filename):
        return jsonify({"error": "Invalid document mimetype, must be image/*"}), 400

    # Check if checkboxes are selected
    all_monetary = True if request.form.get("all_monetary") else False

    try:
        # Save image to local folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Perform inference
        model.predict(file_path)

        # Remove file from local folder
        os.remove(file_path)

        # Post-processing
        all_entities = get_entities(model.confidence_matrix, model.decoded_texts)
        best_entities = get_best_entity_by_confidence(all_entities)
        filtered_entities = filter_entities_by_confidence(all_entities)
        parsed_monetary_entities = parse_monetary_values(all_entities if all_monetary else filtered_entities)

        response = {
            "image_file": filename,
            "entities": all_entities,
            "best_entities": best_entities,
            "filtered_entities": filtered_entities,
            "parsed_monetary_entities": parsed_monetary_entities
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)