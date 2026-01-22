"""
Theme Manager - Handles Dark/Light mode switching with smooth transitions
"""

from PySide6.QtCore import QObject, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor


class ThemeManager(QObject):
    theme_changed = Signal(str)
    
    # Modern Color Palettes
    THEMES = {
        'dark': {
            # Primary Colors
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_tertiary': '#21262d',
            'bg_elevated': '#1c2128',
            
            # Surface Colors
            'surface': '#161b22',
            'surface_hover': '#1f2428',
            'surface_active': '#2d333b',
            
            # Text Colors
            'text_primary': '#e6edf3',
            'text_secondary': '#8b949e',
            'text_muted': '#6e7681',
            'text_link': '#58a6ff',
            
            # Accent Colors
            'accent': '#58a6ff',
            'accent_hover': '#79b8ff',
            'accent_muted': '#388bfd26',
            
            # Status Colors
            'success': '#3fb950',
            'success_muted': '#238636',
            'warning': '#d29922',
            'warning_muted': '#9e6a03',
            'danger': '#f85149',
            'danger_muted': '#da3633',
            'info': '#58a6ff',
            
            # Border Colors
            'border': '#30363d',
            'border_muted': '#21262d',
            'border_subtle': '#1b1f23',
            
            # Shadow
            'shadow': 'rgba(0, 0, 0, 0.4)',
            'shadow_lg': 'rgba(0, 0, 0, 0.6)',
            
            # Sidebar
            'sidebar_bg': '#0d1117',
            'sidebar_hover': '#161b22',
            'sidebar_active': '#1f6feb',
            
            # Card
            'card_bg': '#161b22',
            'card_border': '#30363d',
            
            # Input
            'input_bg': '#0d1117',
            'input_border': '#30363d',
            'input_focus': '#58a6ff',
            
            # Scrollbar
            'scrollbar_bg': '#161b22',
            'scrollbar_thumb': '#30363d',
            'scrollbar_thumb_hover': '#484f58',
        },
        'light': {
            # Primary Colors
            'bg_primary': '#ffffff',
            'bg_secondary': '#f6f8fa',
            'bg_tertiary': '#f0f3f6',
            'bg_elevated': '#ffffff',
            
            # Surface Colors
            'surface': '#ffffff',
            'surface_hover': '#f3f4f6',
            'surface_active': '#ebecf0',
            
            # Text Colors
            'text_primary': '#1f2328',
            'text_secondary': '#656d76',
            'text_muted': '#8c959f',
            'text_link': '#0969da',
            
            # Accent Colors
            'accent': '#0969da',
            'accent_hover': '#0550ae',
            'accent_muted': '#ddf4ff',
            
            # Status Colors
            'success': '#1a7f37',
            'success_muted': '#dafbe1',
            'warning': '#9a6700',
            'warning_muted': '#fff8c5',
            'danger': '#cf222e',
            'danger_muted': '#ffebe9',
            'info': '#0969da',
            
            # Border Colors
            'border': '#d0d7de',
            'border_muted': '#d8dee4',
            'border_subtle': '#eaeef2',
            
            # Shadow
            'shadow': 'rgba(31, 35, 40, 0.12)',
            'shadow_lg': 'rgba(31, 35, 40, 0.2)',
            
            # Sidebar
            'sidebar_bg': '#f6f8fa',
            'sidebar_hover': '#eaeef2',
            'sidebar_active': '#0969da',
            
            # Card
            'card_bg': '#ffffff',
            'card_border': '#d0d7de',
            
            # Input
            'input_bg': '#ffffff',
            'input_border': '#d0d7de',
            'input_focus': '#0969da',
            
            # Scrollbar
            'scrollbar_bg': '#f6f8fa',
            'scrollbar_thumb': '#d0d7de',
            'scrollbar_thumb_hover': '#afb8c1',
        }
    }
    
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self._stylesheet_cache = {}
    
    def get_color(self, color_name: str) -> str:
        """Get color value for current theme"""
        return self.THEMES[self.current_theme].get(color_name, '#ffffff')
    
    def get_colors(self) -> dict:
        """Get all colors for current theme"""
        return self.THEMES[self.current_theme]
    
    def toggle_theme(self) -> str:
        """Toggle between dark and light themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_changed.emit(self.current_theme)
        return self.current_theme
    
    def set_theme(self, theme: str):
        """Set specific theme"""
        if theme in self.THEMES:
            self.current_theme = theme
            self.theme_changed.emit(self.current_theme)
    
    def apply_theme(self, app: QApplication, theme: str = None):
        """Apply theme stylesheet to application"""
        if theme:
            old_theme = self.current_theme
            self.current_theme = theme
            # Emit signal if theme actually changed
            if old_theme != theme:
                self.theme_changed.emit(self.current_theme)
        
        stylesheet = self._generate_stylesheet()
        app.setStyleSheet(stylesheet)
    
    def _generate_stylesheet(self) -> str:
        """Generate QSS stylesheet for current theme"""
        c = self.THEMES[self.current_theme]
        
        return f'''
        /* ========================================
           GLOBAL STYLES
           ======================================== */
        
        QMainWindow, QWidget {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            font-family: "Segoe UI", "SF Pro Display", -apple-system, sans-serif;
        }}
        
        /* ========================================
           SCROLLBAR STYLES
           ======================================== */
        
        QScrollBar:vertical {{
            background: {c['scrollbar_bg']};
            width: 10px;
            margin: 0;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {c['scrollbar_thumb']};
            min-height: 30px;
            border-radius: 5px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {c['scrollbar_thumb_hover']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        
        QScrollBar:horizontal {{
            background: {c['scrollbar_bg']};
            height: 10px;
            margin: 0;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {c['scrollbar_thumb']};
            min-width: 30px;
            border-radius: 5px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {c['scrollbar_thumb_hover']};
        }}
        
        /* ========================================
           LABEL STYLES
           ======================================== */
        
        QLabel {{
            color: {c['text_primary']};
            background: transparent;
        }}
        
        QLabel[class="title"] {{
            font-size: 24px;
            font-weight: 600;
            color: {c['text_primary']};
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 14px;
            color: {c['text_secondary']};
        }}
        
        QLabel[class="heading"] {{
            font-size: 18px;
            font-weight: 600;
            color: {c['text_primary']};
        }}
        
        QLabel[class="muted"] {{
            color: {c['text_muted']};
            font-size: 12px;
        }}
        
        /* ========================================
           BUTTON STYLES
           ======================================== */
        
        QPushButton {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            min-height: 32px;
        }}
        
        QPushButton:hover {{
            background-color: {c['surface_hover']};
            border-color: {c['border_muted']};
        }}
        
        QPushButton:pressed {{
            background-color: {c['surface_active']};
        }}
        
        QPushButton:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_muted']};
            border-color: {c['border_subtle']};
        }}
        
        QPushButton[class="primary"] {{
            background-color: {c['accent']};
            color: white;
            border: none;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {c['accent_hover']};
        }}
        
        QPushButton[class="danger"] {{
            background-color: {c['danger']};
            color: white;
            border: none;
        }}
        
        QPushButton[class="success"] {{
            background-color: {c['success']};
            color: white;
            border: none;
        }}
        
        QPushButton[class="icon"] {{
            background: transparent;
            border: none;
            padding: 8px;
            border-radius: 6px;
        }}
        
        QPushButton[class="icon"]:hover {{
            background-color: {c['surface_hover']};
        }}
        
        /* ========================================
           INPUT STYLES
           ======================================== */
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {c['input_bg']};
            color: {c['text_primary']};
            border: 1px solid {c['input_border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            selection-background-color: {c['accent']};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {c['input_focus']};
            outline: none;
        }}
        
        QLineEdit:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_muted']};
        }}
        
        /* ========================================
           COMBOBOX STYLES
           ======================================== */
        
        QComboBox {{
            background-color: {c['input_bg']};
            color: {c['text_primary']};
            border: 1px solid {c['input_border']};
            border-radius: 6px;
            padding: 8px 12px;
            padding-right: 30px;
            font-size: 13px;
            min-height: 32px;
        }}
        
        QComboBox:hover {{
            border-color: {c['border']};
        }}
        
        QComboBox:focus {{
            border-color: {c['input_focus']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {c['text_secondary']};
            margin-right: 10px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 4px;
            selection-background-color: {c['accent_muted']};
            selection-color: {c['text_primary']};
            outline: none;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 8px 12px;
            border-radius: 4px;
            min-height: 32px;
        }}
        
        QComboBox QAbstractItemView::item:hover {{
            background-color: {c['surface_hover']};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {c['accent_muted']};
        }}
        
        /* ========================================
           SLIDER STYLES
           ======================================== */
        
        QSlider::groove:horizontal {{
            background: {c['border']};
            height: 4px;
            border-radius: 2px;
        }}
        
        QSlider::handle:horizontal {{
            background: {c['accent']};
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {c['accent_hover']};
        }}
        
        QSlider::sub-page:horizontal {{
            background: {c['accent']};
            border-radius: 2px;
        }}
        
        /* ========================================
           CHECKBOX & RADIO STYLES
           ======================================== */
        
        QCheckBox, QRadioButton {{
            color: {c['text_primary']};
            spacing: 8px;
            font-size: 13px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid {c['border']};
            background: {c['input_bg']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {c['accent']};
        }}
        
        QCheckBox::indicator:checked {{
            background: {c['accent']};
            border-color: {c['accent']};
            image: url(qt_app/assets/icons/check.svg);
        }}
        
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 9px;
            border: 1px solid {c['border']};
            background: {c['input_bg']};
        }}
        
        QRadioButton::indicator:checked {{
            background: {c['accent']};
            border: 5px solid {c['input_bg']};
            outline: 1px solid {c['accent']};
        }}
        
        /* ========================================
           TAB WIDGET STYLES
           ======================================== */
        
        QTabWidget::pane {{
            background: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QTabBar::tab {{
            background: transparent;
            color: {c['text_secondary']};
            padding: 10px 20px;
            margin-right: 4px;
            border-bottom: 2px solid transparent;
            font-weight: 500;
        }}
        
        QTabBar::tab:hover {{
            color: {c['text_primary']};
            background: {c['surface_hover']};
        }}
        
        QTabBar::tab:selected {{
            color: {c['accent']};
            border-bottom-color: {c['accent']};
        }}
        
        /* ========================================
           TABLE STYLES
           ======================================== */
        
        QTableWidget, QTableView {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            gridline-color: {c['border_muted']};
            selection-background-color: {c['accent_muted']};
            selection-color: {c['text_primary']};
        }}
        
        QTableWidget::item, QTableView::item {{
            padding: 8px 12px;
            border-bottom: 1px solid {c['border_muted']};
        }}
        
        QTableWidget::item:hover, QTableView::item:hover {{
            background-color: {c['surface_hover']};
        }}
        
        QHeaderView::section {{
            background-color: {c['bg_tertiary']};
            color: {c['text_primary']};
            padding: 10px 12px;
            border: none;
            border-bottom: 1px solid {c['border']};
            font-weight: 600;
        }}
        
        QHeaderView::section:hover {{
            background-color: {c['surface_hover']};
        }}
        
        /* ========================================
           PROGRESS BAR STYLES
           ======================================== */
        
        QProgressBar {{
            background-color: {c['bg_tertiary']};
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {c['accent']};
            border-radius: 4px;
        }}
        
        /* ========================================
           TOOLTIP STYLES
           ======================================== */
        
        QToolTip {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
        }}
        
        /* ========================================
           MENU STYLES
           ======================================== */
        
        QMenu {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 32px 8px 12px;
            border-radius: 4px;
            margin: 2px 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {c['accent_muted']};
        }}
        
        QMenu::separator {{
            height: 1px;
            background: {c['border']};
            margin: 4px 8px;
        }}
        
        /* ========================================
           GROUPBOX STYLES
           ======================================== */
        
        QGroupBox {{
            background-color: {c['card_bg']};
            border: 1px solid {c['card_border']};
            border-radius: 8px;
            margin-top: 16px;
            padding: 16px;
            font-weight: 600;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 8px;
            background-color: {c['card_bg']};
            color: {c['text_primary']};
        }}
        
        /* ========================================
           SPLITTER STYLES
           ======================================== */
        
        QSplitter::handle {{
            background-color: {c['border']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {c['accent']};
        }}
        
        /* ========================================
           FRAME STYLES
           ======================================== */
        
        QFrame[class="card"] {{
            background-color: {c['card_bg']};
            border: 1px solid {c['card_border']};
            border-radius: 12px;
        }}
        
        QFrame[class="divider"] {{
            background-color: {c['border']};
            max-height: 1px;
        }}
        '''
