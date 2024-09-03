import random

class LayoutLMv3Mock:
    def __init__(self):
        self.labels = [
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


    def predict(self, image):
        # This is a mock function that returns dummy data
        num_predictions = random.randint(5, 10)
        predictions = []
        for _ in range(num_predictions):
            predictions.append(
                {
                    "text": f"Sample Text {random.randint(1, 100)}",
                    "label": random.choice(self.labels),
                    "confidence": round(random.uniform(0.1, 1.0), 2),
                    "box": [random.randint(0, 100) for _ in range(4)],
                }
            )
        return predictions