from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from PySide6.QtCore import Signal

class TaskInputUI(QWidget):
    task_started = Signal(str)
    task_stopped = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Guidance Agent")
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("What do you want help with?")
        layout.addWidget(self.label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., Upload a file")
        layout.addWidget(self.input_field)
        
        self.start_btn = QPushButton("Start Guidance")
        self.start_btn.clicked.connect(self.toggle_task)
        layout.addWidget(self.start_btn)
        
        self.setLayout(layout)
        self.is_running = False
        
    def toggle_task(self):
        if not self.is_running:
            task = self.input_field.text().strip()
            if task:
                self.is_running = True
                self.start_btn.setText("Stop Guidance")
                self.input_field.setEnabled(False)
                self.task_started.emit(task)
        else:
            self.is_running = False
            self.start_btn.setText("Start Guidance")
            self.input_field.setEnabled(True)
            self.task_stopped.emit()