from utils.post_processing import (
    filter_entities_by_confidence,
    get_best_entity_by_confidence,
    parse_monetary_values,
)


def test_get_best_entity_by_confidence():
    entities = [
        {"text": "menu", "label": 'menu.nm',"confidence": 0.8},
        {"text": "restaurant", "label": 'menu.nm',"confidence": 0.09},
        {"text": "60.00", "label": "total.total_price","confidence": 0.5},
        {"text": "TOTAL", "label": "total.total_price","confidence": 0.2},
        {"text": "4.60", "label": "sub_total.tax_price","confidence": 0.7},
    ]
    assert get_best_entity_by_confidence(entities) == [
        {"text": "menu", "label": 'menu.nm',"confidence": 0.8},
        {"text": "60.00", "label": "total.total_price","confidence": 0.5},
        {"text": "4.60", "label": "sub_total.tax_price","confidence": 0.7},
    ]


def test_filter_entities_by_confidence():
   entities = [
        {"text": "menu", "label": 'menu.nm',"confidence": 0.8},
        {"text": "60.00", "label": "total.total_price","confidence": 0.5},
        {"text": "4.60", "label": "sub_total.tax_price","confidence": 0.7},
    ]
   filtered = filter_entities_by_confidence(entities)
   assert len(filtered) == 2
   assert all(entity["confidence"] >= 0.6 for entity in filtered)


def test_parse_monetary_values():
    entities = [
        {"text": "menu", "label": 'menu.nm',"confidence": 0.8},
        {"text": "$60.00", "label": "total.total_price", "confidence": 0.5},
        {"text": "4,60", "label": "sub_total.tax_price", "confidence": 0.7},
        {"text": "menu", "label": 'total.changeprice', "confidence": 0.8},
    ]
    parsed = parse_monetary_values(entities)
    assert len(parsed) == 3
    assert parsed[0]["value"] == 60.00
    assert parsed[1]["value"] == 4.60
    assert parsed[2]["value"] is None