import numpy as np
from PIL import Image
import pytesseract
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
import torch

class LayoutLMv3Model:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
        self.model = LayoutLMv3ForTokenClassification.from_pretrained("najwaerrachidy/layoutlmv3-finetuned-cordv2")
        self.encoding = None
        self.confidence_matrix = None
        self.decoded_texts = None


    def preprocess_image(self, image_path):
        # Convert image to PIL Image if it's not already
        if not isinstance(image_path, Image.Image):
            image = Image.open(image_path)
        return image
    

    def encode(self, image):
        # Process image to get its encodings
        self.encoding = {}
        self.encoding = self.processor(image, return_offsets_mapping=False, return_tensors="pt")
        for k,v in self.encoding.items():
            self.encoding[k] = v.to(self.device)

    
    def decode(self):
        # Decode the input_ids back to text
        input_ids = self.encoding['input_ids']
        input_ids_list = input_ids.flatten().tolist()
       
        self.decoded_texts = [self.processor.tokenizer.decode(id, skip_special_tokens=True) for id in input_ids_list]


    def predict(self, image_path):
        # Preprocess image
        image = self.preprocess_image(image_path)

        # Prepare the inputs
        self.encode(image)

        # Decode back to text
        self.decode()

        # Set the path to the Tesseract executable
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

        # Predict for label for each entity, calculate confidence scores, decode text
        with torch.no_grad():
            outputs = self.model(**self.encoding)
            
        # Get the confidence matrix
        self.confidence_matrix = torch.softmax(outputs.logits, dim=-1).squeeze().detach().numpy()