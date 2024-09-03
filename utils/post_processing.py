def get_best_entity_by_confidence(entities):
    return max(entities, key=lambda x: x["confidence"])


def filter_entities_by_confidence(entities, threshold=0.6):
    return [entity for entity in entities if entity["confidence"] >= threshold]


def parse_monetary_values(entities):
    monetary_labels = ["PRICE", "TAX", "TOTAL"]
    for entity in entities:
        if entity["label"] in monetary_labels:
            try:
                entity["value"] = float(
                    entity["text"].replace("$", "").replace(",", "")
                )
            except ValueError:
                entity["value"] = None
    return entities