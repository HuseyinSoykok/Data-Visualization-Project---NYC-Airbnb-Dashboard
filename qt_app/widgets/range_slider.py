"""
Professional Range Slider Widget with Keyboard Input Support
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, 
    QSpinBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush


class DoubleHandleSlider(QSlider):
    """Custom slider with two draggable handles for range selection"""
    
    rangeChanged = Signal(int, int)
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._min_value = self.minimum()
        self._max_value = self.maximum()
        self._low = self.minimum()
        self._high = self.maximum()
        self._pressed_control = None
        self._hover_control = None
        self._handle_width = 12
        self._is_dark = True
        
        self.setMouseTracking(True)
        
    def setRangeLimits(self, minimum, maximum):
        """Set the absolute min/max limits"""
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self._min_value = minimum
        self._max_value = maximum
        
    def setLow(self, low):
        """Set the low value"""
        self._low = max(self._min_value, min(low, self._high))
        self.update()
        
    def setHigh(self, high):
        """Set the high value"""
        self._high = min(self._max_value, max(high, self._low))
        self.update()
        
    def low(self):
        return self._low
        
    def high(self):
        return self._high
        
    def setTheme(self, is_dark):
        """Set the theme"""
        self._is_dark = is_dark
        self.update()
        
    def paintEvent(self, event):
        """Custom paint for dual-handle range slider"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Colors based on theme
        if self._is_dark:
            track_color = QColor("#30363d")
            range_color = QColor("#58a6ff")
            handle_color = QColor("#58a6ff")
            handle_border = QColor("#1f6feb")
        else:
            track_color = QColor("#d0d7de")
            range_color = QColor("#0969da")
            handle_color = QColor("#0969da")
            handle_border = QColor("#0550ae")
            
        # Calculate positions
        groove_y = self.height() // 2 - 2
        groove_height = 4
        groove_width = self.width() - 20
        groove_x = 10
        
        # Draw background track
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(groove_x, groove_y, groove_width, groove_height, 2, 2)
        
        # Calculate handle positions
        span = self._max_value - self._min_value
        if span == 0:
            span = 1
            
        low_pos = groove_x + int((self._low - self._min_value) / span * groove_width)
        high_pos = groove_x + int((self._high - self._min_value) / span * groove_width)
        
        # Draw selected range
        range_width = high_pos - low_pos
        painter.setBrush(QBrush(range_color))
        painter.drawRoundedRect(low_pos, groove_y, range_width, groove_height, 2, 2)
        
        # Draw handles
        handle_y = self.height() // 2
        handle_radius = self._handle_width // 2
        
        # Low handle
        painter.setBrush(QBrush(handle_color))
        painter.setPen(QPen(handle_border, 2))
        painter.drawEllipse(QPoint(low_pos, handle_y), handle_radius, handle_radius)
        
        # High handle
        painter.drawEllipse(QPoint(high_pos, handle_y), handle_radius, handle_radius)
        
    def mousePressEvent(self, event):
        """Handle mouse press to determine which handle to drag"""
        if event.button() == Qt.LeftButton:
            pos = event.position().x()
            
            # Calculate handle positions
            groove_width = self.width() - 20
            groove_x = 10
            span = self._max_value - self._min_value
            if span == 0:
                span = 1
                
            low_pos = groove_x + int((self._low - self._min_value) / span * groove_width)
            high_pos = groove_x + int((self._high - self._min_value) / span * groove_width)
            
            # Determine which handle is closer
            dist_to_low = abs(pos - low_pos)
            dist_to_high = abs(pos - high_pos)
            
            if dist_to_low < dist_to_high:
                self._pressed_control = 'low'
            else:
                self._pressed_control = 'high'
                
            self.mouseMoveEvent(event)
            
    def mouseMoveEvent(self, event):
        """Handle mouse move to drag handles"""
        if self._pressed_control:
            pos = event.position().x()
            
            # Calculate value from position
            groove_width = self.width() - 20
            groove_x = 10
            
            # Clamp position to groove bounds
            pos = max(groove_x, min(pos, groove_x + groove_width))
            
            # Convert position to value
            span = self._max_value - self._min_value
            value = int(self._min_value + (pos - groove_x) / groove_width * span)
            
            # Update appropriate handle
            if self._pressed_control == 'low':
                old_low = self._low
                self.setLow(value)
                if old_low != self._low:
                    self.rangeChanged.emit(self._low, self._high)
            elif self._pressed_control == 'high':
                old_high = self._high
                self.setHigh(value)
                if old_high != self._high:
                    self.rangeChanged.emit(self._low, self._high)
                    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self._pressed_control = None
            
    def sizeHint(self):
        """Provide size hint"""
        from PySide6.QtCore import QSize
        return QSize(200, 30)


class ProfessionalRangeSlider(QWidget):
    """Professional range slider with dual handles and keyboard input"""
    
    rangeChanged = Signal(int, int)
    
    def __init__(self, min_val: int, max_val: int, prefix: str = "$", suffix: str = "", parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val
        self.prefix = prefix
        self.suffix = suffix
        self._is_dark = True
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Input boxes row
        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(8)
        
        # Min input
        min_container = QVBoxLayout()
        min_container.setSpacing(2)
        
        min_label = QLabel("Min")
        min_label.setStyleSheet("font-size: 10px; color: #8b949e;")
        min_container.addWidget(min_label)
        
        self.min_input = QSpinBox()
        self.min_input.setRange(self.min_val, self.max_val)
        self.min_input.setValue(self.min_val)
        self.min_input.setPrefix(self.prefix)
        self.min_input.setSuffix(self.suffix)
        self.min_input.setButtonSymbols(QSpinBox.NoButtons)
        self.min_input.setAlignment(Qt.AlignCenter)
        self._update_spinbox_style(self.min_input)
        self.min_input.valueChanged.connect(self._on_min_input_changed)
        min_container.addWidget(self.min_input)
        
        inputs_layout.addLayout(min_container)
        
        # Separator
        separator = QLabel("—")
        separator.setStyleSheet("color: #8b949e; font-size: 14px;")
        separator.setAlignment(Qt.AlignCenter)
        inputs_layout.addWidget(separator)
        
        # Max input
        max_container = QVBoxLayout()
        max_container.setSpacing(2)
        
        max_label = QLabel("Max")
        max_label.setStyleSheet("font-size: 10px; color: #8b949e;")
        max_container.addWidget(max_label)
        
        self.max_input = QSpinBox()
        self.max_input.setRange(self.min_val, self.max_val)
        self.max_input.setValue(self.max_val)
        self.max_input.setPrefix(self.prefix)
        self.max_input.setSuffix(self.suffix)
        self.max_input.setButtonSymbols(QSpinBox.NoButtons)
        self.max_input.setAlignment(Qt.AlignCenter)
        self._update_spinbox_style(self.max_input)
        self.max_input.valueChanged.connect(self._on_max_input_changed)
        max_container.addWidget(self.max_input)
        
        inputs_layout.addLayout(max_container)
        
        layout.addLayout(inputs_layout)
        
        # Range slider
        self.slider = DoubleHandleSlider(Qt.Horizontal)
        self.slider.setRangeLimits(self.min_val, self.max_val)
        self.slider.setLow(self.min_val)
        self.slider.setHigh(self.max_val)
        self.slider.setMinimumHeight(30)
        self.slider.rangeChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider)
        
    def _update_spinbox_style(self, spinbox):
        """Update spinbox styling"""
        if self._is_dark:
            spinbox.setStyleSheet("""
                QSpinBox {
                    background-color: #161b22;
                    color: #58a6ff;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 13px;
                    font-weight: 600;
                    min-width: 80px;
                }
                QSpinBox:focus {
                    border-color: #58a6ff;
                    background-color: #0d1117;
                }
                QSpinBox:hover {
                    border-color: #58a6ff;
                }
            """)
        else:
            spinbox.setStyleSheet("""
                QSpinBox {
                    background-color: #ffffff;
                    color: #0969da;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 13px;
                    font-weight: 600;
                    min-width: 80px;
                }
                QSpinBox:focus {
                    border-color: #0969da;
                    background-color: #f6f8fa;
                }
                QSpinBox:hover {
                    border-color: #0969da;
                }
            """)
            
    def _on_min_input_changed(self, value):
        """Handle min input change"""
        if value > self.max_input.value():
            self.min_input.setValue(self.max_input.value())
            return
        self.slider.setLow(value)
        self.rangeChanged.emit(value, self.max_input.value())
        
    def _on_max_input_changed(self, value):
        """Handle max input change"""
        if value < self.min_input.value():
            self.max_input.setValue(self.min_input.value())
            return
        self.slider.setHigh(value)
        self.rangeChanged.emit(self.min_input.value(), value)
        
    def _on_slider_changed(self, low, high):
        """Handle slider change"""
        self.min_input.blockSignals(True)
        self.max_input.blockSignals(True)
        
        self.min_input.setValue(low)
        self.max_input.setValue(high)
        
        self.min_input.blockSignals(False)
        self.max_input.blockSignals(False)
        
        self.rangeChanged.emit(low, high)
        
    def get_values(self) -> tuple:
        """Get current range values"""
        return self.min_input.value(), self.max_input.value()
        
    def set_values(self, min_val: int, max_val: int):
        """Set range values"""
        self.min_input.setValue(min_val)
        self.max_input.setValue(max_val)
        self.slider.setLow(min_val)
        self.slider.setHigh(max_val)
        
    def set_theme(self, is_dark: bool):
        """Update theme"""
        self._is_dark = is_dark
        self.slider.setTheme(is_dark)
        self._update_spinbox_style(self.min_input)
        self._update_spinbox_style(self.max_input)
