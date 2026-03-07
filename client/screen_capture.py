import mss
import cv2
import base64
import numpy as np

def capture_frame_base64() -> str:
    """Captures the primary monitor screen and returns a base64 encoded JPEG."""
    with mss.mss() as sct:
        # Monitor 1 is the primary monitor in mss
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        
        # Convert to numpy array (BGRA)
        img = np.array(sct_img)
        
        # Convert BGRA to BGR to save space
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Compress to JPEG
        # Quality 60 is a good trade-off for OCR readability vs websocket speed
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        result, encimg = cv2.imencode('.jpg', img_bgr, encode_param)
        
        if not result:
            return ""
            
        # Convert to base64
        b64_str = base64.b64encode(encimg).decode('utf-8')
        return b64_str