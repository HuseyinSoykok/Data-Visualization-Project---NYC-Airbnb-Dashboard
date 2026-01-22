"""
Animation Helpers - Smooth transitions and visual effects
"""

from PySide6.QtCore import (
    QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup,
    QEasingCurve, QPoint, QSize, Property, Signal, QObject
)
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect


class AnimationManager:
    """Manages animations for widgets"""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """Fade in animation"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        return anim
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300):
        """Fade out animation"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.start()
        
        return anim
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = "left", duration: int = 300):
        """Slide in animation"""
        start_pos = widget.pos()
        
        if direction == "left":
            widget.move(start_pos.x() - 50, start_pos.y())
        elif direction == "right":
            widget.move(start_pos.x() + 50, start_pos.y())
        elif direction == "up":
            widget.move(start_pos.x(), start_pos.y() - 50)
        elif direction == "down":
            widget.move(start_pos.x(), start_pos.y() + 50)
        
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setEndValue(start_pos)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        return anim
    
    @staticmethod
    def scale_in(widget: QWidget, duration: int = 300):
        """Scale in animation"""
        target_size = widget.size()
        widget.resize(0, 0)
        
        anim = QPropertyAnimation(widget, b"size")
        anim.setDuration(duration)
        anim.setEndValue(target_size)
        anim.setEasingCurve(QEasingCurve.OutBack)
        anim.start()
        
        return anim
    
    @staticmethod
    def pulse(widget: QWidget, duration: int = 500):
        """Pulse animation for attention"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setKeyValueAt(0, 1.0)
        anim.setKeyValueAt(0.5, 0.5)
        anim.setKeyValueAt(1.0, 1.0)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        
        return anim
    
    @staticmethod
    def combined_fade_slide(widget: QWidget, direction: str = "up", duration: int = 400):
        """Combined fade and slide animation"""
        # Opacity effect
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        # Create animation group
        group = QParallelAnimationGroup()
        
        # Fade animation
        fade_anim = QPropertyAnimation(effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(0.0)
        fade_anim.setEndValue(1.0)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        group.addAnimation(fade_anim)
        
        # Slide animation
        start_pos = widget.pos()
        offset = 30
        
        if direction == "up":
            widget.move(start_pos.x(), start_pos.y() + offset)
        elif direction == "down":
            widget.move(start_pos.x(), start_pos.y() - offset)
        elif direction == "left":
            widget.move(start_pos.x() + offset, start_pos.y())
        elif direction == "right":
            widget.move(start_pos.x() - offset, start_pos.y())
        
        slide_anim = QPropertyAnimation(widget, b"pos")
        slide_anim.setDuration(duration)
        slide_anim.setEndValue(start_pos)
        slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        group.addAnimation(slide_anim)
        
        group.start()
        
        return group


class StaggeredAnimation(QObject):
    """Animate multiple widgets with staggered timing"""
    
    finished = Signal()
    
    def __init__(self, widgets: list, animation_type: str = "fade_in", 
                 stagger_delay: int = 50, duration: int = 300):
        super().__init__()
        self.widgets = widgets
        self.animation_type = animation_type
        self.stagger_delay = stagger_delay
        self.duration = duration
        self.animations = []
    
    def start(self):
        """Start the staggered animation"""
        from PySide6.QtCore import QTimer
        
        for i, widget in enumerate(self.widgets):
            QTimer.singleShot(
                i * self.stagger_delay,
                lambda w=widget: self._animate_widget(w)
            )
    
    def _animate_widget(self, widget: QWidget):
        """Animate a single widget"""
        if self.animation_type == "fade_in":
            anim = AnimationManager.fade_in(widget, self.duration)
        elif self.animation_type == "slide_in":
            anim = AnimationManager.slide_in(widget, "up", self.duration)
        elif self.animation_type == "combined":
            anim = AnimationManager.combined_fade_slide(widget, "up", self.duration)
        else:
            return
        
        self.animations.append(anim)


class TransitionManager:
    """Manages page transitions"""
    
    @staticmethod
    def cross_fade(stack_widget, new_index: int, duration: int = 300):
        """Cross-fade transition between stack widget pages"""
        current = stack_widget.currentWidget()
        target = stack_widget.widget(new_index)
        
        if current == target:
            return
        
        # Fade out current
        if current:
            AnimationManager.fade_out(current, duration // 2)
        
        # Switch and fade in new
        from PySide6.QtCore import QTimer
        QTimer.singleShot(duration // 2, lambda: stack_widget.setCurrentIndex(new_index))
        QTimer.singleShot(duration // 2, lambda: AnimationManager.fade_in(target, duration // 2))
    
    @staticmethod
    def slide_transition(stack_widget, new_index: int, direction: str = "left", duration: int = 400):
        """Slide transition between stack widget pages"""
        target = stack_widget.widget(new_index)
        stack_widget.setCurrentIndex(new_index)
        AnimationManager.slide_in(target, direction, duration)
