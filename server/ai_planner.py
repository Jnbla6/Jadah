import os
import json
from typing import List, Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
from shared.schemas import ScreenElement
from server.models import AIPlanOutput

# تحميل المتغيرات من ملف .env
load_dotenv()

# تهيئة عميل Gemini (سيقرأ المفتاح تلقائياً من GEMINI_API_KEY)
client = genai.Client()

def get_next_step(task: str, elements: List[ScreenElement]) -> Optional[AIPlanOutput]:
    """Uses Gemini API to find the target element matching the task."""
    
    # تجهيز قائمة العناصر الموجودة على الشاشة ليفهمها الذكاء الاصطناعي
    element_descriptions = []
    for el in elements:
        cx = el.x + (el.width // 2)
        cy = el.y + (el.height // 2)
        element_descriptions.append(f'Text: "{el.text}" at (x: {cx}, y: {cy})')
        
    elements_text = "\n".join(element_descriptions)
    
    # رسالة التعليمات (Prompt)
    prompt = f"""
    The user wants to: "{task}"
    
    Here are the text elements currently visible on the user's screen:
    {elements_text}
    
    Determine the single best element the user needs to interact with to accomplish their task.
    If no relevant elements are found, return pointer_x and pointer_y as null, and give a waiting instruction.
    """
    
    try:
        # استدعاء نموذج Gemini 2.5 Flash السريع والمجاني
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful UI navigation assistant.",
                temperature=0.0,
                # إجبار النموذج على إرجاع JSON يطابق هيكل AIPlanOutput تماماً
                response_mime_type="application/json",
                response_schema=AIPlanOutput,
            ),
        )
        
        # تحويل النص العائد من Gemini إلى كائن Python
        data = json.loads(response.text)
        return AIPlanOutput(**data)
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None