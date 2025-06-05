from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
import json

class AnnotationTool:
    ARROW = "arrow"
    CIRCLE = "circle"
    CONE = "cone"
    RECTANGLE = "rectangle"
    TRACKING_BOX = "tracking_box"

class AnnotationOverlay(QWidget):
    # Signal emitted when a tracking box is created
    tracking_box_created = pyqtSignal(QRectF, float)  # (bounds, timestamp)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Drawing state
        self.drawing = False
        self.last_point = None
        self.current_path = None
        self.current_color = QColor(255, 0, 0)  # Default to red
        self.current_tool = AnnotationTool.ARROW
        
        # Store annotations with timestamps
        self.annotations = {}  # Key: timestamp, Value: list of (tool, path, color)
        
        # Tracking state
        self.tracked_objects = {}  # Key: id, Value: (timestamp, bounds) list
        self.current_timestamp = 0.0
        
    def set_tool(self, tool):
        """Set the current drawing tool"""
        self.current_tool = tool
        
    def set_color(self, color):
        """Set the current drawing color"""
        self.current_color = color
        
    def set_current_time(self, timestamp):
        """Update current video timestamp"""
        self.current_timestamp = timestamp
        self.update()

    def start_drawing(self, pos):
        """Start drawing at the given position"""
        self.drawing = True
        self.last_point = pos
        self.current_path = QPainterPath()
        self.current_path.moveTo(pos)
        self.update()

    def continue_drawing(self, pos):
        """Continue drawing to the new position"""
        if not self.drawing or not self.last_point:
            return
            
        if self.current_tool in [AnnotationTool.TRACKING_BOX, AnnotationTool.RECTANGLE]:
            # Create rectangle from start point to current
            self.current_path = QPainterPath()
            rect = QRectF(self.last_point, pos).normalized()
            self.current_path.addRect(rect)
        elif self.current_tool == AnnotationTool.ARROW:
            self.current_path = QPainterPath()
            self.current_path.moveTo(self.last_point)
            self.current_path.lineTo(pos)
        elif self.current_tool == AnnotationTool.CIRCLE:
            self.current_path = QPainterPath()
            radius = ((pos - self.last_point).manhattanLength()) / 2
            center = self.last_point + (pos - self.last_point) / 2
            self.current_path.addEllipse(center, radius, radius)
        elif self.current_tool == AnnotationTool.CONE:
            self.current_path = QPainterPath()
            # Draw cone as triangle
            self.current_path.moveTo(self.last_point)
            width = pos.x() - self.last_point.x()
            height = pos.y() - self.last_point.y()
            self.current_path.lineTo(self.last_point.x() - width/2, pos.y())
            self.current_path.lineTo(self.last_point.x() + width/2, pos.y())
            self.current_path.closeSubpath()
        
        self.update()

    def end_drawing(self, timestamp):
        """Finish drawing and save the annotation"""
        if not self.drawing or not self.current_path:
            return
            
        if self.current_tool == AnnotationTool.TRACKING_BOX:
            # Emit signal for tracking initialization
            rect = self.current_path.boundingRect()
            self.tracking_box_created.emit(rect, timestamp)
        else:
            if timestamp not in self.annotations:
                self.annotations[timestamp] = []
            self.annotations[timestamp].append((
                self.current_tool,
                self.current_path,
                self.current_color
            ))
            
        self.drawing = False
        self.current_path = None
        self.last_point = None
        self.update()

    def update_tracking(self, object_id, timestamp, bounds):
        """Update tracking data for an object"""
        if object_id not in self.tracked_objects:
            self.tracked_objects[object_id] = []
        self.tracked_objects[object_id].append((timestamp, bounds))
        self.update()

    def clear_annotations(self):
        """Clear all annotations and tracking data"""
        self.annotations.clear()
        self.tracked_objects.clear()
        self.update()

    def save_annotations(self, filename):
        """Save annotations to a JSON file"""
        data = {
            'annotations': {},
            'tracking': {}
        }
        
        # Save static annotations
        for timestamp, annotations in self.annotations.items():
            data['annotations'][str(timestamp)] = [
                {
                    'tool': tool,
                    'path': self._serialize_path(path),
                    'color': color.name()
                }
                for tool, path, color in annotations
            ]
            
        # Save tracking data
        for object_id, tracking_data in self.tracked_objects.items():
            data['tracking'][str(object_id)] = [
                {
                    'timestamp': timestamp,
                    'bounds': {
                        'x': bounds.x(),
                        'y': bounds.y(),
                        'width': bounds.width(),
                        'height': bounds.height()
                    }
                }
                for timestamp, bounds in tracking_data
            ]
            
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_annotations(self, filename):
        """Load annotations from a JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            
        self.clear_annotations()
        
        # Load static annotations
        for timestamp_str, annotations in data.get('annotations', {}).items():
            timestamp = float(timestamp_str)
            self.annotations[timestamp] = [
                (
                    anno['tool'],
                    self._deserialize_path(anno['path']),
                    QColor(anno['color'])
                )
                for anno in annotations
            ]
            
        # Load tracking data
        for object_id_str, tracking_data in data.get('tracking', {}).items():
            object_id = int(object_id_str)
            self.tracked_objects[object_id] = [
                (
                    item['timestamp'],
                    QRectF(
                        item['bounds']['x'],
                        item['bounds']['y'],
                        item['bounds']['width'],
                        item['bounds']['height']
                    )
                )
                for item in tracking_data
            ]
            
        self.update()
        
    def _serialize_path(self, path):
        """Convert QPainterPath to serializable format"""
        elements = []
        for i in range(path.elementCount()):
            e = path.elementAt(i)
            elements.append({
                'type': e.type,
                'x': e.x,
                'y': e.y
            })
        return elements
        
    def _deserialize_path(self, elements):
        """Convert serialized format back to QPainterPath"""
        path = QPainterPath()
        for e in elements:
            if e['type'] == QPainterPath.MoveToElement:
                path.moveTo(e['x'], e['y'])
            elif e['type'] == QPainterPath.LineToElement:
                path.lineTo(e['x'], e['y'])
            elif e['type'] == QPainterPath.CurveToElement:
                # Handle curves if needed
                pass
        return path

    def paintEvent(self, event):
        """Draw all annotations and current drawing preview"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw saved annotations for current timestamp
        if self.current_timestamp in self.annotations:
            for tool, path, color in self.annotations[self.current_timestamp]:
                painter.setPen(QPen(color, 2, Qt.SolidLine))
                if tool == AnnotationTool.ARROW:
                    self._draw_arrow(painter, path)
                else:
                    painter.drawPath(path)
                    if tool == AnnotationTool.CONE:
                        # Fill cone with semi-transparent color
                        fill_color = QColor(color)
                        fill_color.setAlpha(128)
                        painter.fillPath(path, fill_color)

        # Draw tracked objects
        for object_id, tracking_data in self.tracked_objects.items():
            # Find and interpolate position at current timestamp
            bounds = self._interpolate_tracking(tracking_data, self.current_timestamp)
            if bounds:
                painter.setPen(QPen(self.current_color, 2, Qt.DashLine))
                painter.drawRect(bounds)
                # Draw object ID
                painter.drawText(bounds.topLeft(), f"Object {object_id}")

        # Draw current path preview
        if self.drawing and self.current_path:
            painter.setPen(QPen(self.current_color, 2, Qt.SolidLine))
            if self.current_tool == AnnotationTool.ARROW:
                self._draw_arrow(painter, self.current_path)
            else:
                painter.drawPath(self.current_path)
                if self.current_tool == AnnotationTool.CONE:
                    fill_color = QColor(self.current_color)
                    fill_color.setAlpha(128)
                    painter.fillPath(self.current_path, fill_color)

    def _interpolate_tracking(self, tracking_data, timestamp):
        """Interpolate object position at given timestamp"""
        if not tracking_data:
            return None
            
        # Find surrounding keyframes
        prev_data = None
        next_data = None
        for time, bounds in sorted(tracking_data):
            if time <= timestamp:
                prev_data = (time, bounds)
            elif time > timestamp:
                next_data = (time, bounds)
                break
                
        if not prev_data:
            return next_data[1] if next_data else None
        if not next_data:
            return prev_data[1]
            
        # Linear interpolation
        prev_time, prev_bounds = prev_data
        next_time, next_bounds = next_data
        ratio = (timestamp - prev_time) / (next_time - prev_time)
        
        return QRectF(
            prev_bounds.x() + (next_bounds.x() - prev_bounds.x()) * ratio,
            prev_bounds.y() + (next_bounds.y() - prev_bounds.y()) * ratio,
            prev_bounds.width() + (next_bounds.width() - prev_bounds.width()) * ratio,
            prev_bounds.height() + (next_bounds.height() - prev_bounds.height()) * ratio
        )

    def _draw_arrow(self, painter, path):
        """Helper to draw an arrow with a triangle head"""
        if path.elementCount() < 2:
            return

        start = path.elementAt(0)
        end = path.elementAt(path.elementCount() - 1)
        
        # Draw the line
        painter.drawPath(path)
        
        # Calculate arrow head
        angle = 30  # degrees
        arrow_size = 20  # pixels
        dx = end.x - start.x
        dy = end.y - start.y
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return
            
        dx, dy = dx / length, dy / length
        
        # Calculate arrow head points
        import math
        rad_angle = math.radians(angle)
        p1 = QPoint(
            int(end.x - arrow_size * (dx * math.cos(rad_angle) + dy * math.sin(rad_angle))),
            int(end.y - arrow_size * (dy * math.cos(rad_angle) - dx * math.sin(rad_angle)))
        )
        p2 = QPoint(
            int(end.x - arrow_size * (dx * math.cos(rad_angle) - dy * math.sin(rad_angle))),
            int(end.y - arrow_size * (dy * math.cos(rad_angle) + dx * math.sin(rad_angle)))
        )
        
        # Draw arrow head
        arrow_head = QPainterPath()
        arrow_head.moveTo(end.x, end.y)
        arrow_head.lineTo(p1.x(), p1.y())
        arrow_head.lineTo(p2.x(), p2.y())
        arrow_head.lineTo(end.x, end.y)
        
        painter.fillPath(arrow_head, self.current_color)