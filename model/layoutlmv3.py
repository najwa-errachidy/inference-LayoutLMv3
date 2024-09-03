from PIL import Image
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
import torch

class LayoutLMv3:
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
        self.id2label = {v: k for v, k in enumerate(self.labels)}

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
        self.model = LayoutLMv3ForTokenClassification.from_pretrained("najwaerrachidy/layoutlmv3-finetuned-cordv2")
        self.encoding = {}
        self.entities = []
    

    def encode(self, image_path):
        # Process image to get its encodings
        image = Image.open(image_path)
        self.encoding = self.processor(image, return_offsets_mapping=False, return_tensors="pt")
        for k,v in self.encoding.items():
            self.encoding[k] = v.to(self.device)


    def predict(self):
        # Predict for label for each entity, calculate confidence scores, decode text
        outputs = self.model(**self.encoding)
        confidence = [max(l) for l in outputs.logits[0].detach().numpy()]
        ids = outputs.logits.argmax(-1).squeeze().tolist()
        
        input_ids = self.encoding['input_ids']
        input_ids_list = input_ids.flatten().tolist()

        # Decode the input_ids back to text
        decoded_texts = [self.processor.tokenizer.decode(id, skip_special_tokens=True) for id in input_ids_list]
        
        for i in range(len(ids)):
            self.entities.append({
                'text' : decoded_texts[i],
                'label' : self.id2label[ids[i]],
                'confidence' : confidence[i]
            })