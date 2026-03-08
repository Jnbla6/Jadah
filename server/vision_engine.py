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
    
    # We will group words that belong to the same block, paragraph, and line
    current_group = None

    for i in range(n_boxes):
        text = d['text'][i].strip()
        conf = int(d['conf'][i])
        
        # Filter out empty text and low confidence predictions
        if int(conf) > 40 and text:
            block_num = d['block_num'][i]
            par_num = d['par_num'][i]
            line_num = d['line_num'][i]
            
            x = d['left'][i]
            y = d['top'][i]
            w = d['width'][i]
            h = d['height'][i]
            
            if current_group is None:
                current_group = {
                    'text': text, 'x': x, 'y': y, 'w': w, 'h': h,
                    'block': block_num, 'par': par_num, 'line': line_num
                }
            else:
                # Same line check
                if (current_group['block'] == block_num and 
                    current_group['par'] == par_num and 
                    current_group['line'] == line_num and
                    # ensure words are relatively close horizontally (e.g., < 30px apart)
                    x - (current_group['x'] + current_group['w']) < 30):
                    
                    # Merge them
                    current_group['text'] += " " + text
                    # New bounding box
                    new_x = min(current_group['x'], x)
                    new_y = min(current_group['y'], y)
                    new_w = max(current_group['x'] + current_group['w'], x + w) - new_x
                    new_h = max(current_group['y'] + current_group['h'], y + h) - new_y
                    
                    current_group['x'] = new_x
                    current_group['y'] = new_y
                    current_group['w'] = new_w
                    current_group['h'] = new_h
                else:
                    # Save the old group and start a new one
                    elements.append(ScreenElement(
                        text=current_group['text'],
                        x=current_group['x'],
                        y=current_group['y'],
                        width=current_group['w'],
                        height=current_group['h']
                    ))
                    current_group = {
                        'text': text, 'x': x, 'y': y, 'w': w, 'h': h,
                        'block': block_num, 'par': par_num, 'line': line_num
                    }
                    
    # Append the last group
    if current_group is None == False:
        elements.append(ScreenElement(
            text=current_group['text'],
            x=current_group['x'],
            y=current_group['y'],
            width=current_group['w'],
            height=current_group['h']
        ))
            
    return elements