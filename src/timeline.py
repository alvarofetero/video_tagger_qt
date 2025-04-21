from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QPoint

class TimelineWidget(QWidget):
    tag_clicked = pyqtSignal(float)

    def __init__(self, get_duration, get_tags, parent=None):
        super().__init__(parent)
        self.get_duration = get_duration
        self.get_tags = get_tags
        self.setMinimumHeight(40)
        self.highlighted_index = None
        self.current_time = 0.0

    def set_current_time(self, time_sec):
        self.current_time = time_sec
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        duration = self.get_duration()
        tags = self.get_tags()

        if not duration:
            return

        painter.fillRect(self.rect(), QColor(230, 230, 230))

        font = QFont("Arial", 8)
        painter.setFont(font)

        for i, tag in enumerate(tags):
            if tag["start"] is not None and tag["end"] is not None:
                start_ratio = tag["start"] / duration
                end_ratio = tag["end"] / duration
                x = int(start_ratio * self.width())
                width = int((end_ratio - start_ratio) * self.width())
                width = max(width, 2)

                color = QColor(255, 100, 100, 200)
                if i == self.highlighted_index:
                    color = QColor(255, 150, 0, 230)

                # Bloque de tag
                painter.fillRect(x, 15, width, 20, color)

                # Texto encima
                tag_label = f"Tag {i + 1}"
                text_width = painter.fontMetrics().boundingRect(tag_label).width()
                text_x = x + (width - text_width) // 2
                text_x = max(0, min(text_x, self.width() - text_width))

                painter.setPen(Qt.black)
                painter.drawText(text_x, 12, tag_label)
                # Línea de tiempo de reproducción actual
        
        if duration > 0:
            progress_ratio = self.current_time / duration
            x = int(progress_ratio * self.width())
           # Línea azul de posición actual
            line_color = QColor(50, 50, 250)
            painter.setPen(line_color)
            painter.drawLine(x, 0, x, self.height())

            # Triángulo encima
            triangle_height = 8
            triangle_width = 10
            points = [
                QPoint(x, 0),
                QPoint(x - triangle_width // 2, triangle_height),
                QPoint(x + triangle_width // 2, triangle_height)
            ]
            painter.setBrush(line_color)
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(*points)



    def mousePressEvent(self, event: QMouseEvent):
        duration = self.get_duration()
        tags = self.get_tags()

        if not duration or not tags:
            return

        click_x = event.x()
        clicked_ratio = click_x / self.width()
        clicked_time = clicked_ratio * duration

        for i, tag in enumerate(tags):
            if tag["start"] <= clicked_time <= tag["end"]:
                self.highlighted_index = i
                self.update()
                self.tag_clicked.emit(tag["start"])
                break
