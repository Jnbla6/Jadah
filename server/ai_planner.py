import json
from typing import List, Optional
import ollama
from shared.schemas import ScreenElement
from server.models import AIPlanOutput

def get_next_step(task: str, elements: List[ScreenElement]) -> Optional[AIPlanOutput]:
    task_lower = task.lower()

    # 1. SMART INTENT
    search_words = []
    target_exact = None
    is_save_flow = False
    
    if "save" in task_lower:
        search_words.extend(["file", "save"])
        target_exact = "save"
        is_save_flow = True
    elif "file" in task_lower:
        search_words.extend(["file"])
        target_exact = "file"
    elif "edit" in task_lower:
        search_words.extend(["edit"])
        target_exact = "edit"
    elif "close" in task_lower or "tap" in task_lower or "window" in task_lower:
        search_words.extend(["x", "close"]) 
        target_exact = "x"
    elif "view" in task_lower:
        search_words.extend(["view"])
        target_exact = "view"
    else:
        ignore = {"how", "to", "a", "in", "the", "on", "where", "is", "click", "code", "vs", "window", "tap", "btn", "press"}
        search_words = [w for w in task_lower.split() if w not in ignore]

    # 2. SPATIAL UI SHIELD 🛡️ (الوعي المكاني)
    ui_elements = []
    bad_chars = ['"', "'", "‘", "’", "“", "”", "_", "(", ")", "=", "{", "}", "[", "]", ";", "*"]
    
    # Assume standard 1080p or 1440p screen for center document detection
    # We heavily penalize coordinates that are in the middle of the screen (the "canvas")
    
    for el in elements:
        text_raw = el.text.strip()
        text_lower = text_raw.lower()
        
        if len(text_lower) < 1 or any(char in text_raw for char in bad_chars):
            continue
            
        # تحديد مناطق الواجهة الحقيقية وتجاهل منتصف الشاشة (منطقة الأكواد أو المستند)
        # Top ribbon/menu (e.g. File, Edit, View, Save) is almost always Y < 120
        is_top_menu = el.y < 120 
        
        # Left sidebar (e.g. VSCode explorer, settings)
        is_left_dropdown = el.x < 400 and el.y < 800 
        
        # Top right (e.g. Close X, user profile)
        is_top_right = el.x > 1000 and el.y < 120 
        
        # Center Screen "Danger Zone" (Document canvas where text is just text, not buttons)
        is_center_canvas = (el.x > 300 and el.x < 1500) and (el.y > 150 and el.y < 800)
        
        # If it's in the center canvas, it's highly likely just text in a document, NOT a button!
        if is_center_canvas:
            continue
            
        if not (is_top_menu or is_left_dropdown or is_top_right):
            continue

        if text_lower == "x" and "x" in search_words:
            ui_elements.append(el)
            continue

        if text_lower in search_words or any(word == text_lower for word in search_words):
            ui_elements.append(el)

    # 3. SUPER SNIPER TARGET LOCK 🎯 (التوجيه العبقري ومنع القفز)
    if target_exact:
        target_btn = None
        step_num = 1
        
        if is_save_flow:
            # نبحث عن زر Save (تطابق دقيق)
            exact_saves = [el for el in ui_elements if el.text.lower() == "save"]
            if exact_saves:
                # إذا وجدنا أكثر من Save (مثل Save و Save As)، نرتبها من الأعلى للأسفل!
                exact_saves.sort(key=lambda el: el.y)
                target_btn = exact_saves[0] # نختار الأعلى دائماً!
                step_num = 2
            else:
                # إذا لم نجد Save، نبحث عن File في القائمة العلوية
                exact_files = [el for el in ui_elements if el.text.lower() == "file" and el.y < 80]
                if exact_files:
                    exact_files.sort(key=lambda el: el.y)
                    target_btn = exact_files[0]
                    step_num = 1
        else:
            # للكلمات الأخرى غير الـ Save
            exact_matches = [el for el in ui_elements if el.text.lower() == target_exact]
            if exact_matches:
                exact_matches.sort(key=lambda el: el.y)
                target_btn = exact_matches[0]

        # رسم السهم إذا وجدنا الهدف
        if target_btn:
            print(f"🔒 Sniper Locked precisely on: '{target_btn.text}' at Y:{target_btn.y}")
            return AIPlanOutput(
                step=step_num,
                instruction=f"Click '{target_btn.text}'",
                pointer_x=target_btn.x + (target_btn.width // 2),
                pointer_y=target_btn.y + (target_btn.height // 2),
                visual="arrow"
            )

    # 4. NORMAL AI FLOW (للأوامر المعقدة)
    if not ui_elements: return None

    element_descriptions = [f'ID: {i} | Text: "{el.text}"' for i, el in enumerate(ui_elements[:8])]
    prompt = f'Task: "{task}"\nUI Elements: {" | ".join(element_descriptions)}\nOutput ONLY JSON: {{"step": 1, "instruction": "Click here", "element_id": 0}}'
    
    try:
        response = ollama.chat(model='qwen2.5:0.5b', messages=[{'role': 'user', 'content': prompt}], format='json', options={'temperature': 0.0})
        data = json.loads(response['message']['content'])
        chosen_id = data.get("element_id")
        
        if chosen_id is not None and 0 <= chosen_id < len(ui_elements):
            chosen_element = ui_elements[chosen_id]
            return AIPlanOutput(
                step=data.get("step", 1),
                instruction=data.get("instruction", "Click here"),
                pointer_x=chosen_element.x + (chosen_element.width // 2),
                pointer_y=chosen_element.y + (chosen_element.height // 2),
                visual="arrow"
            )
    except Exception:
        pass
        
    return None