from utils.post_processing import (
    filter_entities_by_confidence,
    get_best_entity_by_confidence,
    parse_monetary_values,
)


def test_get_best_entity_by_confidence():
    entities = [
        {"text": "A", "confidence": 0.8},
        {"text": "B", "confidence": 0.9},
        {"text": "C", "confidence": 0.7},
    ]
    assert get_best_entity_by_confidence(entities)["text"] == "B"


def test_filter_entities_by_confidence():
    entities = [
        {"text": "A", "confidence": 0.8},
        {"text": "B", "confidence": 0.5},
        {"text": "C", "confidence": 0.7},
    ]
    filtered = filter_entities_by_confidence(entities)
    assert len(filtered) == 2
    assert all(entity["confidence"] >= 0.6 for entity in filtered)


def test_parse_monetary_values():
    entities = [
        {"text": "$10.99", "label": "PRICE"},
        {"text": "Not a number", "label": "TOTAL"},
        {"text": "$2,000.00", "label": "TAX"},
    ]
    parsed = parse_monetary_values(entities)
    assert parsed[0]["value"] == 10.99
    assert parsed[1]["value"] is None
    assert parsed[2]["value"] == 2000.00
