"""
Modern Sidebar Navigation Component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QFont, QColor


class NavItem(QPushButton):
    """Single navigation item in sidebar"""
    
    def __init__(self, icon: str, text: str, key: str, parent=None):
        super().__init__(parent)
        self.key = key
        self._active = False
        self._is_dark = True
        
        self.setText(f"  {icon}  {text}")
        self.setFixedHeight(44)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self._update_style()
    
    def set_active(self, active: bool):
        self._active = active
        self.setChecked(active)
        self._update_style()
    
    def set_theme(self, is_dark: bool):
        self._is_dark = is_dark
    
    def _update_style(self):
        if self._active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(88, 166, 255, 0.15);
                    color: #58a6ff;
                    border: none;
                    border-left: 3px solid #58a6ff;
                    border-radius: 0;
                    text-align: left;
                    padding-left: 16px;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
        else:
            if self._is_dark:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #8b949e;
                        border: none;
                        border-left: 3px solid transparent;
                        border-radius: 0;
                        text-align: left;
                        padding-left: 16px;
                        font-size: 14px;
                        font-weight: 400;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.05);
                        color: #e6edf3;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #656d76;
                        border: none;
                        border-left: 3px solid transparent;
                        border-radius: 0;
                        text-align: left;
                        padding-left: 16px;
                        font-size: 14px;
                        font-weight: 400;
                    }
                    QPushButton:hover {
                        background-color: rgba(0, 0, 0, 0.05);
                        color: #1f2328;
                    }
                """)


class SidebarSection(QWidget):
    """Section within sidebar with title and items"""
    
    def __init__(self, title: str = None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 8, 0, 8)
        self.layout.setSpacing(2)
        
        if title:
            title_label = QLabel(title.upper())
            title_label.setStyleSheet("""
                QLabel {
                    color: #6e7681;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                    padding: 8px 20px 4px 20px;
                    background: transparent;
                }
            """)
            self.layout.addWidget(title_label)
    
    def add_item(self, item: NavItem):
        self.layout.addWidget(item)


class ModernSidebar(QWidget):
    """Modern collapsible sidebar with navigation"""
    
    navigation_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = True
        self._expanded_width = 260
        self._collapsed_width = 70
        self._items = {}
        self._current_key = None
        
        self.setFixedWidth(self._expanded_width)
        self.setObjectName("sidebar")
        self._setup_ui()
        self._setup_animation()
    
    def _setup_ui(self):
        self._is_dark = True
        
        # Base style first (widgets not yet created)
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #0d1117;
                border-right: 1px solid #21262d;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 12, 0)
        
        # Logo/Title
        self.title_label = QLabel("🏠 NYC Airbnb")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
        """)
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # Collapse button
        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setFixedSize(36, 36)
        self.collapse_btn.setCursor(Qt.PointingHandCursor)
        self.collapse_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8b949e;
                border: none;
                border-radius: 6px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.collapse_btn.clicked.connect(self.toggle_collapse)
        header_layout.addWidget(self.collapse_btn)
        
        main_layout.addWidget(header)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #21262d;")
        main_layout.addWidget(divider)
        
        # Scroll area for nav items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        self.nav_container = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 8, 0, 8)
        self.nav_layout.setSpacing(0)
        
        scroll.setWidget(self.nav_container)
        main_layout.addWidget(scroll, 1)
        
        # Footer
        footer = QWidget()
        footer.setFixedHeight(60)
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(12, 8, 12, 12)
        
        # Theme toggle in footer
        theme_container = QWidget()
        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setContentsMargins(8, 0, 8, 0)
        
        self.theme_label = QLabel("🌙 Dark Mode")
        self.theme_label.setStyleSheet("color: #8b949e; font-size: 13px; background: transparent;")
        theme_layout.addWidget(self.theme_label)
        
        theme_layout.addStretch()
        
        from qt_app.widgets.custom_widgets import AnimatedToggle
        self.theme_toggle = AnimatedToggle()
        self.theme_toggle.setChecked(True)
        theme_layout.addWidget(self.theme_toggle)
        
        footer_layout.addWidget(theme_container)
        
        main_layout.addWidget(footer)
    
    def _setup_animation(self):
        self._animation = QPropertyAnimation(self, b"minimumWidth")
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.setDuration(250)
        
        self._animation2 = QPropertyAnimation(self, b"maximumWidth")
        self._animation2.setEasingCurve(QEasingCurve.OutCubic)
        self._animation2.setDuration(250)
    
    def add_section(self, title: str = None) -> SidebarSection:
        """Add a new section to the sidebar"""
        section = SidebarSection(title)
        self.nav_layout.addWidget(section)
        return section
    
    def add_nav_item(self, section: SidebarSection, icon: str, text: str, key: str):
        """Add navigation item to a section"""
        item = NavItem(icon, text, key)
        item.clicked.connect(lambda: self._on_item_clicked(key))
        section.add_item(item)
        self._items[key] = item
        return item
    
    def add_spacer(self):
        """Add flexible spacer"""
        self.nav_layout.addStretch()
    
    def _on_item_clicked(self, key: str):
        """Handle navigation item click"""
        if self._current_key == key:
            return
        
        # Deactivate previous
        if self._current_key and self._current_key in self._items:
            self._items[self._current_key].set_active(False)
        
        # Activate current
        self._current_key = key
        if key in self._items:
            self._items[key].set_active(True)
        
        self.navigation_changed.emit(key)
    
    def set_active(self, key: str):
        """Programmatically set active nav item"""
        self._on_item_clicked(key)
    
    def toggle_collapse(self):
        """Toggle sidebar collapsed state"""
        self._expanded = not self._expanded
        
        target_width = self._expanded_width if self._expanded else self._collapsed_width
        
        self._animation.setStartValue(self.width())
        self._animation.setEndValue(target_width)
        self._animation2.setStartValue(self.width())
        self._animation2.setEndValue(target_width)
        
        self._animation.start()
        self._animation2.start()
        
        # Update visibility of text elements
        self.title_label.setVisible(self._expanded)
        self.theme_label.setVisible(self._expanded)
        
        for item in self._items.values():
            if self._expanded:
                item.setText(item.text())  # Restore full text
            # In collapsed mode, you might want to show only icons
    
    def is_expanded(self) -> bool:
        return self._expanded
    
    def set_theme(self, is_dark: bool):
        """Update sidebar theme"""
        self._is_dark = is_dark
        self._update_sidebar_style()
        self._update_items_style()
    
    def _update_sidebar_style(self):
        """Update sidebar colors based on theme"""
        if self._is_dark:
            self.setStyleSheet("""
                QWidget#sidebar {
                    background-color: #0d1117;
                    border-right: 1px solid #21262d;
                }
            """)
            self.title_label.setStyleSheet("QLabel { color: #e6edf3; font-size: 16px; font-weight: 600; background: transparent; }")
            self.theme_label.setStyleSheet("color: #8b949e; font-size: 13px; background: transparent;")
            self.collapse_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #8b949e;
                    border: none;
                    border-radius: 6px;
                    font-size: 18px;
                }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }
            """)
        else:
            self.setStyleSheet("""
                QWidget#sidebar {
                    background-color: #f6f8fa;
                    border-right: 1px solid #d0d7de;
                }
            """)
            self.title_label.setStyleSheet("QLabel { color: #1f2328; font-size: 16px; font-weight: 600; background: transparent; }")
            self.theme_label.setStyleSheet("color: #656d76; font-size: 13px; background: transparent;")
            self.collapse_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #656d76;
                    border: none;
                    border-radius: 6px;
                    font-size: 18px;
                }
                QPushButton:hover { background-color: rgba(0, 0, 0, 0.05); }
            """)
    
    def _update_items_style(self):
        """Update nav items for theme"""
        for item in self._items.values():
            item.set_theme(self._is_dark)
            item._update_style()
