import json
import pytest
from app.app import app


@pytest.fixture
def simple_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def max_document_size_client():
    app.config["TESTING"] = True
    app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024  # 3 MB max file size
    with app.test_client() as client:
        yield client


def test_process_document_success_checkbox_off(simple_client):
    data = {
        "document": (open("tests/test_image.jpg", "rb"), "test_image.jpg"),
    }
    response = simple_client.post(
        "/process_document", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    result = json.loads(response.data)
    assert "image_file" in result
    assert "entities" in result
    assert "best_entities" in result
    assert "filtered_entities" in result
    assert "parsed_monetary_entities" in result
    # Assert that all 'confidence' values in 'parsed_monetary_entities' are >= 0.6
    assert all(entity["confidence"] >= 0.6 for entity in result["parsed_monetary_entities"])


def test_process_document_success_checkbox_on(simple_client):
    data = {
        "document": (open("tests/test_image.jpg", "rb"), "test_image.jpg"),
        "all_monetary": "on"  # Mimic checkbox being checked
    }
    response = simple_client.post(
        "/process_document", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    result = json.loads(response.data)
    assert "image_file" in result
    assert "entities" in result
    assert "best_entities" in result
    assert "filtered_entities" in result
    assert "parsed_monetary_entities" in result


def test_process_document_no_file(simple_client):
    response = simple_client.post("/process_document")
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result
    assert result["error"] == "No document found"


def test_process_document_empty_file(simple_client):
    data = {"document": (b"", "")}
    response = simple_client.post(
        "/process_document", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result
    assert result["error"] == "Empty document"


def test_process_document_large_file(max_document_size_client):
    # This file is a 3.28 MB file (image)
    data = {
        "document": (open("tests/test_image_large.jpg", "rb"), "test_image_large.jpg")
    }
    response = max_document_size_client.post(
        "/process_document", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 413  # Payload too large
    result = json.loads(response.data)
    assert "error" in result
    assert result["error"] == "File too large"


def test_process_document_invalid_mimetype(simple_client):
    data = {
        "document": (
            open("tests/test_image_wrong_extension.txt", "rb"),
            "test_image_wrong_extension.txt"
        )
    }
    response = simple_client.post(
        "/process_document", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result
    assert result["error"] == "Invalid document type, must be image"