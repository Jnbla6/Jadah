from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os

class TaskInputUI(QWidget):
    task_started = Signal(str)
    task_stopped = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Guidance Agent")
        self.resize(400, 320)
        self.setStyleSheet("""
            QWidget {
                background-color: #fdfdfd;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#TitleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#SubtitleLabel {
                font-size: 13px;
                color: #7f8c8d;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #e74c3c;
            }
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #922b21;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)
        
        # Logo placeholder
        self.logo_label = QLabel()
        # Resolve absolute path to the logo dynamically
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "jadahlogo.png")
        pixmap = QPixmap(logo_path)
        
        if pixmap.isNull():
            self.logo_label.setText("LOGO")
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #bdc3c7;
                    background-color: #f0f3f4;
                    border: 2px dashed #bdc3c7;
                    border-radius: 10px;
                }
            """)
            self.logo_label.setFixedSize(150, 150)
        else:
            self.logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.logo_label.setAlignment(Qt.AlignCenter)
            
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_label)
        logo_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(logo_layout)
        
        # Titles
        self.title_label = QLabel("Jadah Agent")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("ماذا تريد ان اساعدك عليه اليوم؟")
        self.subtitle_label.setObjectName("SubtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle_label)
        
        # Input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., Upload a file, fill a form...")
        layout.addWidget(self.input_field)
        
        # Spacer
        layout.addSpacing(5)
        
        # Button
        self.start_btn = QPushButton("خذني على الجادة")
        self.start_btn.clicked.connect(self.toggle_task)
        layout.addWidget(self.start_btn)
        
        layout.addStretch()
        self.setLayout(layout)
        self.is_running = False
        
    def toggle_task(self):
        if not self.is_running:
            task = self.input_field.text().strip()
            if task:
                self.is_running = True
                self.start_btn.setText("إيقاف الجادة")
                self.start_btn.setStyleSheet("""
                    QPushButton { background-color: #7f8c8d; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 14px; font-weight: bold; }
                    QPushButton:hover { background-color: #95a5a6; }
                    QPushButton:pressed { background-color: #34495e; }
                """)
                self.input_field.setEnabled(False)
                self.task_started.emit(task)
        else:
            self.is_running = False
            self.start_btn.setText("خذني على الجادة")
            self.start_btn.setStyleSheet("")
            self.input_field.setEnabled(True)
            self.task_stopped.emit()