from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QPolygon, QFont

class OverlayRenderer(QWidget):
    def __init__(self):
        super().__init__()
        # Make window transparent and always on top, click-through
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool | 
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Cover the entire screen
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        
        self.target_point = None
        self.instruction_text = ""
        
    def update_instruction(self, instruction_data: dict):
        """Called via signal when websocket receives new coordinates."""
        pointer = instruction_data.get("pointer")
        if pointer and pointer.get("x") is not None and pointer.get("y") is not None:
            self.target_point = QPoint(pointer["x"], pointer["y"])
        else:
            self.target_point = None
            
        self.instruction_text = instruction_data.get("instruction", "")
        # Trigger a repaint
        self.update()
        
    def clear_instruction(self):
        self.target_point = None
        self.instruction_text = ""
        self.update()

    def paintEvent(self, event):
        if not self.target_point:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        tx = self.target_point.x()
        ty = self.target_point.y()

        # 1. Draw Highlight Circle
        painter.setPen(QPen(QColor(255, 0, 0, 150), 4))
        painter.setBrush(QColor(255, 0, 0, 50))
        painter.drawEllipse(tx - 25, ty - 25, 50, 50)

        # 2. Draw Arrow pointing to the circle
        # Arrow starts offset to the top-left of the target
        offset = 60
        start_x, start_y = tx - offset, ty - offset
        end_x, end_y = tx - 30, ty - 30 # Stop at the edge of the circle

        painter.setPen(QPen(QColor(255, 0, 0, 255), 6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(start_x, start_y, end_x, end_y)

        # Arrow head
        arrow_head = QPolygon([
            QPoint(end_x, end_y),
            QPoint(end_x - 15, end_y),
            QPoint(end_x, end_y - 15)
        ])
        painter.setBrush(QColor(255, 0, 0, 255))
        painter.drawPolygon(arrow_head)

        # 3. Draw Text Bubble
        if self.instruction_text:
            painter.setFont(QFont("Arial", 14, QFont.Bold))
            text_rect = painter.fontMetrics().boundingRect(self.instruction_text)
            
            # Position text above the arrow start
            box_rect = QRect(start_x - text_rect.width()//2 - 10, 
                             start_y - text_rect.height() - 20, 
                             text_rect.width() + 20, 
                             text_rect.height() + 10)

            # Draw Bubble
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 200))
            painter.drawRoundedRect(box_rect, 10, 10)

            # Draw Text
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(box_rect, Qt.AlignCenter, self.instruction_text)