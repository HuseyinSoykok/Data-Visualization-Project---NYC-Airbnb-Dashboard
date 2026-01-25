"""
Custom Widgets - Modern UI Components
"""

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGraphicsDropShadowEffect, QSizePolicy,
    QSpacerItem
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property, QSize
from PySide6.QtGui import QColor, QPainter, QPainterPath, QFont, QIcon


class ModernCard(QFrame):
    """Modern card widget with shadow and hover effects"""
    
    clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self._setup_shadow()
        self._hover = False
        self.setCursor(Qt.PointingHandCursor)
        
    def _setup_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        self._hover = True
        effect = self.graphicsEffect()
        if effect:
            effect.setBlurRadius(30)
            effect.setYOffset(8)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hover = False
        effect = self.graphicsEffect()
        if effect:
            effect.setBlurRadius(20)
            effect.setYOffset(4)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class StatCard(ModernCard):
    """Statistics card with icon, value, and label"""
    
    def __init__(self, icon: str, value: str, label: str, color: str = "#58a6ff", parent=None):
        super().__init__(parent)
        self.color = color
        self._setup_ui(icon, value, label)
        
    def _setup_ui(self, icon: str, value: str, label: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 28px; color: {self.color}; background: transparent;")
        layout.addWidget(icon_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {self.color};
            background: transparent;
        """)
        layout.addWidget(self.value_label)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setProperty("class", "muted")
        label_widget.setStyleSheet("font-size: 13px; background: transparent;")
        layout.addWidget(label_widget)
        
        layout.addStretch()
        
        self.setMinimumHeight(140)
        self.setMaximumHeight(160)
    
    def set_value(self, value: str):
        self.value_label.setText(value)


class MissingDataBadge(QWidget):
    """Badge to indicate missing data in visualizations"""
    
    def __init__(self, count: int, percentage: float, column: str = "", parent=None):
        super().__init__(parent)
        self.count = count
        self.percentage = percentage
        self.column = column
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        
        # Warning icon
        icon_label = QLabel("⚠️")
        icon_label.setStyleSheet("font-size: 14px; background: transparent;")
        layout.addWidget(icon_label)
        
        # Text
        text = f"{self.count} missing"
        if self.column:
            text = f"{self.column}: {text} ({self.percentage}%)"
        else:
            text = f"{text} ({self.percentage}%)"
        
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                color: #d29922;
                font-size: 11px;
                font-weight: 500;
                background: transparent;
            }
        """)
        layout.addWidget(text_label)
        
        # Style the badge
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(210, 153, 34, 0.15);
                border: 1px solid rgba(210, 153, 34, 0.3);
                border-radius: 8px;
            }
        """)
        self.setMaximumWidth(250)


class UncertaintyIndicator(QWidget):
    """Indicator showing confidence intervals and uncertainty"""
    
    def __init__(self, value: float, ci_lower: float, ci_upper: float, 
                 label: str = "", unit: str = "", parent=None):
        super().__init__(parent)
        self.value = value
        self.ci_lower = ci_lower
        self.ci_upper = ci_upper
        self.label = label
        self.unit = unit
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # Label
        if self.label:
            label_widget = QLabel(self.label)
            label_widget.setStyleSheet("""
                QLabel {
                    color: #8b949e;
                    font-size: 11px;
                    background: transparent;
                }
            """)
            layout.addWidget(label_widget)
        
        # Value with confidence interval
        margin = abs(self.value - self.ci_lower)
        value_text = f"{self.unit}{self.value:.1f} ± {self.unit}{margin:.1f}"
        
        value_label = QLabel(value_text)
        value_label.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 14px;
                font-weight: 600;
                background: transparent;
            }
        """)
        layout.addWidget(value_label)
        
        # Range display
        range_text = f"95% CI: {self.unit}{self.ci_lower:.1f} - {self.unit}{self.ci_upper:.1f}"
        range_label = QLabel(range_text)
        range_label.setStyleSheet("""
            QLabel {
                color: #6e7681;
                font-size: 10px;
                font-style: italic;
                background: transparent;
            }
        """)
        layout.addWidget(range_label)
        
        # Style the container
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(88, 166, 255, 0.1);
                border: 1px solid rgba(88, 166, 255, 0.3);
                border-radius: 8px;
            }
        """)


class DataQualityBadge(QWidget):
    """Badge showing data quality score"""
    
    def __init__(self, score: float, parent=None):
        super().__init__(parent)
        self.score = score
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        
        # Quality icon based on score
        if self.score >= 95:
            icon = "✅"
            color = "#3fb950"
        elif self.score >= 85:
            icon = "✓"
            color = "#58a6ff"
        elif self.score >= 70:
            icon = "⚠️"
            color = "#d29922"
        else:
            icon = "❌"
            color = "#f85149"
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 14px; background: transparent;")
        layout.addWidget(icon_label)
        
        text_label = QLabel(f"Data Quality: {self.score:.1f}%")
        text_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 11px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        layout.addWidget(text_label)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {color}22;
                border: 1px solid {color}44;
                border-radius: 8px;
            }}
        """)
        self.setMaximumWidth(180)


class IconButton(QPushButton):
    """Modern icon button with hover effects"""
    
    def __init__(self, icon_text: str = "", tooltip: str = "", parent=None):
        super().__init__(icon_text, parent)
        self.setProperty("class", "icon")
        self.setToolTip(tooltip)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                border-radius: 8px;
            }
        """)


class AnimatedToggle(QWidget):
    """Modern animated toggle switch"""
    
    toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._circle_position = 3
        self.setFixedSize(50, 26)
        self.setCursor(Qt.PointingHandCursor)
        
        self._animation = QPropertyAnimation(self, b"circle_position")
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.setDuration(200)
    
    def get_circle_position(self):
        return self._circle_position
    
    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    circle_position = Property(float, get_circle_position, set_circle_position)
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked: bool):
        self._checked = checked
        self._animation.setEndValue(27 if checked else 3)
        self._animation.start()
        self.toggled.emit(checked)
    
    def toggle(self):
        self.setChecked(not self._checked)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
        super().mousePressEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        bg_color = QColor("#58a6ff") if self._checked else QColor("#30363d")
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 50, 26, 13, 13)
        
        # Draw circle
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(int(self._circle_position), 3, 20, 20)


class SectionHeader(QWidget):
    """Section header with title and optional action"""
    
    def __init__(self, title: str, action_text: str = None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 12)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            background: transparent;
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        if action_text:
            action_btn = QPushButton(action_text)
            action_btn.setProperty("class", "primary")
            action_btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(action_btn)
            self.action_button = action_btn


class Badge(QLabel):
    """Modern badge/tag component"""
    
    COLORS = {
        'default': ('#8b949e', '#21262d'),
        'primary': ('#58a6ff', '#388bfd26'),
        'success': ('#3fb950', '#23863626'),
        'warning': ('#d29922', '#9e6a0326'),
        'danger': ('#f85149', '#da363326'),
    }
    
    def __init__(self, text: str, variant: str = "default", parent=None):
        super().__init__(text, parent)
        self._set_style(variant)
    
    def _set_style(self, variant: str):
        text_color, bg_color = self.COLORS.get(variant, self.COLORS['default'])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }}
        """)


class Divider(QFrame):
    """Horizontal divider line"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setProperty("class", "divider")
        self.setFixedHeight(1)


class LoadingSpinner(QWidget):
    """Modern loading spinner"""
    
    def __init__(self, size: int = 40, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._angle = 0
        self._timer_id = None
    
    def start(self):
        if self._timer_id is None:
            self._timer_id = self.startTimer(16)  # ~60fps
    
    def stop(self):
        if self._timer_id is not None:
            self.killTimer(self._timer_id)
            self._timer_id = None
    
    def timerEvent(self, event):
        self._angle = (self._angle + 5) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        size = min(self.width(), self.height())
        rect = self.rect().adjusted(4, 4, -4, -4)
        
        # Draw arc
        painter.setPen(Qt.NoPen)
        
        # Background circle
        painter.setBrush(QColor("#30363d"))
        painter.drawEllipse(rect)
        
        # Spinning arc
        path = QPainterPath()
        path.arcMoveTo(rect, self._angle)
        path.arcTo(rect, self._angle, 90)
        
        from PySide6.QtGui import QPen
        pen = QPen(QColor("#58a6ff"), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, self._angle * 16, 90 * 16)


class EmptyState(QWidget):
    """Empty state placeholder with icon and message"""
    
    def __init__(self, icon: str, title: str, description: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 64px; opacity: 0.5; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #8b949e;
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                font-size: 14px;
                color: #6e7681;
                background: transparent;
            """)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)


class SearchBox(QWidget):
    """Modern search input with icon"""
    
    textChanged = Signal(str)
    
    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QLineEdit
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(f"🔍 {placeholder}")
        self.input.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.input)
    
    def text(self) -> str:
        return self.input.text()
    
    def clear(self):
        self.input.clear()
