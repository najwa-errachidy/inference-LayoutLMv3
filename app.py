import json

from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import RequestEntityTooLarge

from model.layoutlmv3_mock import LayoutLMv3Mock
from utils.post_processing import (
    filter_entities_by_confidence,
    get_best_entity_by_confidence,
    parse_monetary_values,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024  # 3 MB max file size

# to be replaced by actual model class after
model = LayoutLMv3Mock()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def upload_form():
    return render_template("upload.html")


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
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid document mimetype, must be image/*"}), 400

    try:
        # Perform inference (mock)
        predictions = model.predict(file)

        # Post-processing
        best_entity = get_best_entity_by_confidence(predictions)
        filtered_entities = filter_entities_by_confidence(predictions)
        parsed_entities = parse_monetary_values(filtered_entities)

        response = {
            "best_entity": best_entity,
            "filtered_entities": filtered_entities,
            "parsed_entities": parsed_entities,
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)