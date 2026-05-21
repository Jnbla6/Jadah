# 🎯 Jadah AI | جادة AI

<p align="center">
  <a href="#arabic">العربية</a> • 
  <a href="#english">English</a>
</p>

---

## <a id="arabic"></a> 🇸🇦 جادة AI - مساعد سطح المكتب للإرشاد البصري التفاعلي

**جادة AI** هو مساعد ذكي متقدم لسطح المكتب يعمل كمرشد بصري تفاعلي في الوقت الفعلي (Real-Time). تم تصميم المشروع كأداة تعليمية وتدريبية موجهة للموظفين؛ حيث لا يقوم بأتمتة المهام أو تنفيذها نيابة عن المستخدم، بل يركز بشكل كامل على **توجيه وتعليم الموظف خطوة بخطوة**. 

يقوم النظام بـ "النظر" إلى شاشتك وفهم مكونات واجهة المستخدم (UI)، ومن ثم يرسم أسهماً وإشارات مرئية دقيقة تشير مباشرة إلى العناصر والأزرار التي يجب النقر عليها لإتمام المهمة بنجاح، مما يمنح الموظف تجربة تدريبية تفاعلية وعملية.

يعتمد المشروع على هيكلية **العميل والخادم (Client-Server Architecture)** لفصل العمليات وضمان أداء سلس وتجاوب فوري أثناء تحليل واجهات الشاشة.

---

### ✨ المميزات الرئيسية
* **إرشاد بصري تفاعلي:** رسم أشكال توجيهية وأسهم مرئية على شاشة المستخدم مباشرة.
* **التركيز التدريبي:** تعليم الموظف كيفية إنجاز العمل بنفسه بدلاً من الأتمتة الكاملة.
* **معالجة محلية:** دمج نماذج الذكاء الاصطناعي محلياً للحفاظ على أمان وسرية بيانات الشاشة.
* **هيكلية مرنة:** فصل واجهة العميل (Client) عن محرك المعالجة والخادم (Server).

---

### 📋 المتطلبات الأساسية
قبل البدء في إعداد وتشغيل المشروع، تأكد من تثبيت البرامج التالية على جهازك:

1. **Python 3.9 أو أحدث:** تأكد من تفعيل خيار إضافة بايثون إلى مسار النظام (`Add Python to PATH`) أثناء التثبيت.
2. **Ollama:** يجب أن يكون مثبتاً ومستضافاً محلياً على جهازك لتشغيل النماذج الذكية.
3. **Tesseract OCR (لنظام ويندوز):**
   * قم بتحميل نسخة التثبيت الخاصة بويندوز من الرابط التالي: [UB-Mannheim Tesseract Installers](https://github.com/UB-Mannheim/tesseract/wiki).
   * ثبّت البرنامج في المسار الافتراضي التالي: `C:\Program Files\Tesseract-OCR`.
   * > ⚠️ **ملاحظة:** إذا قمت بتغيير مسار التثبيت الافتراضي، يجب عليك تحديث المتغير `tesseract_cmd` بالمسار الجديد داخل ملف `server/vision_engine.py`.

---

### 🛠️ التثبيت والإعداد

**1. استنساخ المشروع والانتقال للمجلد**
افتح موجه الأوامر (Terminal) وانتقل إلى المجلد الرئيسي للمشروع:
```bash
cd Jadah
```

**2. تثبيت المكتبات الاعتمادية**
قم بتشغيل الأمر التالي لتثبيت كافة مكتبات بايثون المطلوبة (مثل `FastAPI`, `OpenCV`, `PySide6`, `Google GenAI` وغيرها):
```bash
pip install -r requirements.txt
```

---

### 🚀 تشغيل المشروع

يعمل المشروع بنظام (العميل/الخادم)، لذا يجب تشغيل الخادم أولاً ليقوم بمعالجة الرؤية الحاسوبية، ثم تشغيل واجهة العميل.

**الخطوة 1: تشغيل الخادم (Server Backend)**
في نافذة الـ Terminal الأولى، قم بتشغيل محرك الرؤية والخادم الخلفي:
```bash
python server/main.py
```

**الخطوة 2: تشغيل العميل (Client UI)**
افتح نافذة Terminal ثانية وجديدة، ثم قم بتشغيل واجهة المستخدم لسطح المكتب:
```bash
python client/main.py
```

---

### 📂 هيكل المجلدات الأساسي
```text
Jadah/
├── client/                 # واجهة المستخدم والتفاعل لسطح المكتب (PySide6)
│   └── main.py
├── server/                 # خادم المعالجة الخلفي ومحرك الرؤية الحاسوبية
│   ├── main.py
│   └── vision_engine.py    # الملف المسؤول عن تحليل الشاشة والتكامل مع Tesseract
├── requirements.txt        # ملف المكتبات والاعتماديات المطلوبة للمشروع
└── README.md               # ملف دليل المشروع
```

---

## <a id="english"></a> 🇬🇧 Jadah AI - Desktop Assistant for Interactive Visual Guidance

**Jadah AI** is an advanced desktop assistant that acts as a real-time, interactive visual guide. Purpose-built for employee training and onboarding, Jadah AI does not automate tasks or execute actions on behalf of the user. Instead, its core mission is to **teach and guide employees step-by-step**.

The system "looks" at your screen, comprehends the layout of the User Interface (UI), and draws precise visual arrows and annotations pointing directly to the exact buttons or elements you need to click to successfully accomplish your task.

The project is built upon a robust **Client-Server Architecture** to isolate compute-heavy computer vision processes from the responsive desktop UI.

---

### ✨ Key Features
* **Interactive Visual Guidance:** Draws clear, real-time instructional arrows and shapes directly onto the screen.
* **Educational Focus:** Empowers employees to learn by doing, shifting away from full task automation.
* **Privacy-First Processing:** Seamlessly integrates with locally hosted models to ensure screen data remains secure.
* **Decoupled Architecture:** Clean separation between the desktop client and the background backend processor.

---

### 📋 Prerequisites
Ensure you have the following software components installed and configured before running the application:

1. **Python 3.9 or higher:** Ensure the "Add Python to PATH" option is checked during installation.
2. **Ollama:** Must be installed and hosted locally on your machine to drive the intelligent model orchestration.
3. **Tesseract OCR (for Windows):**
   * Download the Windows binaries from: [UB-Mannheim Tesseract Installers](https://github.com/UB-Mannheim/tesseract/wiki).
   * Install it directly to the default directory: `C:\Program Files\Tesseract-OCR`.
   * > ⚠️ **Note:** If you opt to install Tesseract in an alternative directory, you must explicitly update the `tesseract_cmd` path variable inside `server/vision_engine.py`.

---

### 🛠️ Installation & Setup

**1. Navigate to Project Root**
Open your preferred Terminal interface and navigate into the root directory of the repository:
```bash
cd Jadah
```

**2. Install Required Dependencies**
Execute the following command to install all necessary Python packages (including `FastAPI`, `OpenCV`, `PySide6`, `Google GenAI`, and others):
```bash
pip install -r requirements.txt
```

---

### 🚀 Execution Guide

Since the system relies on a decoupled client-server framework, you must initialize the backend computer vision server before firing up the desktop client interface.

**Step 1: Launch the Backend Server**
In your first terminal window, spin up the processing server:
```bash
python server/main.py
```

**Step 2: Launch the Desktop Client**
Open a secondary terminal window and execute the following command to initialize the user overlay application:
```bash
python client/main.py
```

---

### 📂 Directory Structure
```text
Jadah/
├── client/                 # Desktop graphical interface and overlay layer (PySide6)
│   └── main.py
├── server/                 # Processing backend and vision processing environment
│   ├── main.py
│   └── vision_engine.py    # Core screen analysis engine and Tesseract pipeline
├── requirements.txt        # Global project dependencies mapping
└── README.md               # Repository documentation
```
