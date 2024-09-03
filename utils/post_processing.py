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

def get_best_entity_by_confidence(confidence_matrix, decoded_texts):
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


def filter_entities_by_confidence(entities, threshold=0.6):
    return [entity for entity in entities if entity["confidence"] >= threshold]


def parse_monetary_values(entities):
    for entity in entities:
        if entity["label"] in monetary_labels:
            try:
                entity_text = copy(entity["text"])
                entity["value"] = float(
                    entity_text.replace("$", "").replace(",", ".")
                )
            except ValueError:
                entity["value"] = None
    return entities