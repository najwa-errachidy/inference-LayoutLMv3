import numpy as np
from copy import copy

labels = [
    'menu.cnt',
    'menu.discountprice',
    'menu.etc',
    'menu.itemsubtotal',
    'menu.nm',
    'menu.num',
    'menu.price',
    'menu.sub_cnt',
    'menu.sub_etc',
    'menu.sub_nm',
    'menu.sub_price',
    'menu.sub_unitprice',
    'menu.unitprice',
    'menu.vatyn',
    'sub_total.discount_price',
    'sub_total.etc',
    'sub_total.othersvc_price',
    'sub_total.service_price',
    'sub_total.subtotal_price',
    'sub_total.tax_price',
    'total.cashprice',
    'total.changeprice',
    'total.creditcardprice',
    'total.emoneyprice',
    'total.menuqty_cnt',
    'total.menutype_cnt',
    'total.total_etc',
    'total.total_price',
    'void_menu.nm',
    'void_menu.price'
]

id2label = {v: k for v, k in enumerate(labels)}

monetary_labels = [
    # Menu
    'menu.unitprice',
    'menu.price',
    'menu.itemsubtotal',
    'menu.sub_unitprice',
    'menu.sub_price',

    # Voice Menu
    'void_menu.price',

    # Subtotal
    'sub_total.subtotal_price',
    'sub_total.service_price',
    'sub_total.othersvc_price',
    'sub_total.tax_price',

    # Total
    'total.total_price',
    'total.cashprice',
    'total.changeprice',
    'total.creditcardprice',
    'total.emoneyprice'
]


def get_entities(confidence_matrix, decoded_texts):
    # Build list of all entities
    ids = confidence_matrix.argmax(-1).tolist()
    confidence = [max(l) for l in confidence_matrix]

    entities = []
    for i in range(len(ids)):
        entities.append({
            'text' : decoded_texts[i],
            'label' : id2label[ids[i]],
            'confidence' : confidence[i].item()
        })
    return entities


def get_best_entity_by_confidence(entities):
    # Initialize a dictionary to store the maximum confidence entries for each label
    max_confidence_dict = {}

    for entity in entities:
        label = entity['label']
        # If the label is not in the dictionary or the current confidence is greater than the stored one
        if label not in max_confidence_dict or entity['confidence'] > max_confidence_dict[label]['confidence']:
            max_confidence_dict[label] = entity
    return list(max_confidence_dict.values())


def filter_entities_by_confidence(entities, threshold=0.6):
    return [entity for entity in entities if entity["confidence"] >= threshold]


def parse_monetary_values(entities):
    parsed_monetary_entities = []
    for entity in entities:
        if entity["label"] in monetary_labels:
            try:
                entity_text = copy(entity["text"])
                entity["value"] = float(
                    entity_text.replace("$", "").replace(",", ".")
                )
            except ValueError:
                entity["value"] = None
            parsed_monetary_entities.append(entity)
    return parsed_monetary_entities