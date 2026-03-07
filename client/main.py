import sys
from PySide6.QtWidgets import QApplication
from client.task_input_ui import TaskInputUI
from client.overlay_renderer import OverlayRenderer
from client.websocket_client import WebSocketWorker

def main():
    app = QApplication(sys.argv)
    
    # 1. Initialize windows and workers
    overlay = OverlayRenderer()
    worker = WebSocketWorker("ws://localhost:8000/ws")
    
    # 2. Wire up signals
    # When server sends an instruction, update the overlay
    worker.instruction_received.connect(overlay.update_instruction)
    
    # When user starts a task, set the task in the worker and start streaming
    def on_task_started(task_text):
        worker.set_task(task_text)
        worker.start() # Starts the QThread
        
    def on_task_stopped():
        worker.stop()
        overlay.clear_instruction()
        
    # 3. Setup Task UI
    task_ui = TaskInputUI()
    task_ui.task_started.connect(on_task_started)
    task_ui.task_stopped.connect(on_task_stopped)
    
    # 4. Show Windows
    task_ui.show()
    overlay.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()