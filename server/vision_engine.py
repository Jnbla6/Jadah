import base64
import numpy as np
import cv2
import pytesseract
from pytesseract import Output
from typing import List
from shared.schemas import ScreenElement

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_frame(image_base64: str) -> List[ScreenElement]:
    """Decodes base64 image and runs OCR to find text elements."""
    # Decode base64 to OpenCV image
    img_data = base64.b64decode(image_base64)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if img is None:
        return []

    # Run Tesseract OCR
    # Note: Ensure tesseract is in your PATH. If on Windows, you might need:
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    
    elements = []
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        text = d['text'][i].strip()
        conf = int(d['conf'][i])
        
        # Filter out empty text and low confidence predictions
        if int(conf) > 40 and text:
            elements.append(ScreenElement(
                text=text,
                x=d['left'][i],
                y=d['top'][i],
                width=d['width'][i],
                height=d['height'][i]
            ))
            
    return elements