from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QPolygon, QFont

class OverlayRenderer(QWidget):
    def __init__(self):
        super().__init__()
        # نافذة شفافة وتطفو فوق كل شيء
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool | 
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        
        self.target_point = None
        self.instruction_text = ""
        
    def update_instruction(self, instruction_data: dict):
        pointer = instruction_data.get("pointer")
        if pointer and pointer.get("x") is not None and pointer.get("y") is not None:
            self.target_point = QPoint(pointer["x"], pointer["y"])
        else:
            self.target_point = None
            
        self.instruction_text = instruction_data.get("instruction", "")
        self.is_target_reached = instruction_data.get("is_target_reached", False)
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
        
        # الإحداثيات الدقيقة القادمة من الذكاء الاصطناعي
        tx = self.target_point.x()
        ty = self.target_point.y()

        # 1. رسم نقطة قنص صغيرة (Dot) في منتصف الكلمة تماماً
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 50, 50, 255))
        painter.drawEllipse(tx - 4, ty - 4, 8, 8)

        # 2. رسم دائرة استهداف أنيقة وشفافة
        painter.setPen(QPen(QColor(255, 50, 50, 200), 3))
        painter.setBrush(QColor(255, 50, 50, 40))
        painter.drawEllipse(tx - 25, ty - 25, 50, 50)

        # 3. رسم سهم يشير من الأعلى إلى الأسفل بشكل مستقيم ومباشر
        start_x, start_y = tx, ty - 90
        end_x, end_y = tx, ty - 30 

        painter.setPen(QPen(QColor(255, 50, 50, 255), 6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(start_x, start_y, end_x, end_y)

        # رأس السهم المتجه للأسفل
        arrow_head = QPolygon([
            QPoint(end_x, end_y),
            QPoint(end_x - 12, end_y - 15),
            QPoint(end_x + 12, end_y - 15)
        ])
        painter.setBrush(QColor(255, 50, 50, 255))
        painter.drawPolygon(arrow_head)

        # 4. رسم صندوق النص بشكل عصري فوق السهم
        if getattr(self, 'is_target_reached', False):
            painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
            text_rect = painter.fontMetrics().boundingRect("✨ اضغط هنا! ✨")
            
            box_rect = QRect(tx - text_rect.width()//2 - 20, 
                             ty - text_rect.height() - 40, 
                             text_rect.width() + 40, 
                             text_rect.height() + 20)

            # Green glowing background
            painter.setPen(QPen(QColor(46, 204, 113, 255), 3))
            painter.setBrush(QColor(39, 174, 96, 230))
            painter.drawRoundedRect(box_rect, 10, 10)

            painter.setPen(QColor(255, 255, 255))
            painter.drawText(box_rect, Qt.AlignCenter, "✨ اضغط هنا! ✨")
            
            # Draw a subtle green ring instead of red
            painter.setPen(QPen(QColor(46, 204, 113, 255), 4))
            painter.setBrush(QColor(46, 204, 113, 50))
            painter.drawEllipse(tx - 30, ty - 30, 60, 60)
            
        elif self.instruction_text:
            painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
            text_rect = painter.fontMetrics().boundingRect(self.instruction_text)
            
            box_rect = QRect(start_x - text_rect.width()//2 - 15, 
                             start_y - text_rect.height() - 25, 
                             text_rect.width() + 30, 
                             text_rect.height() + 15)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(30, 30, 30, 230)) # خلفية داكنة أنيقة
            painter.drawRoundedRect(box_rect, 8, 8)

            painter.setPen(QColor(255, 255, 255))
            painter.drawText(box_rect, Qt.AlignCenter, self.instruction_text)