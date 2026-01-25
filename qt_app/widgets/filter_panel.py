"""
Filter Panel - Modern filtering sidebar component
Enhanced with full app_en.py filter capabilities
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QSlider, QFrame, QScrollArea,
    QSizePolicy, QSpacerItem, QGroupBox, QSpinBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from typing import Dict, List

from qt_app.widgets.range_slider import ProfessionalRangeSlider


class FilterSection(QFrame):
    """A collapsible filter section"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("filterSection")
        self._expanded = True
        self._is_dark = True
        self._setup_ui(title)
    
    def _setup_ui(self, title: str):
        self.setStyleSheet("""
            QFrame#filterSection {
                background-color: transparent;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(8)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel(title)
        self._update_title_style()
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setFixedSize(24, 24)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self._update_toggle_style()
        self.toggle_btn.clicked.connect(self._toggle)
        header_layout.addWidget(self.toggle_btn)
        
        layout.addWidget(header)
        
        # Content container
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        layout.addWidget(self.content)
    
    def _toggle(self):
        self._expanded = not self._expanded
        self.content.setVisible(self._expanded)
        self.toggle_btn.setText("▼" if self._expanded else "▶")
    
    def add_widget(self, widget: QWidget):
        self.content_layout.addWidget(widget)
    
    def set_theme(self, is_dark: bool):
        self._is_dark = is_dark
        self._update_title_style()
        self._update_toggle_style()
    
    def _update_title_style(self):
        color = "#e6edf3" if self._is_dark else "#1f2328"
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: 600;
                color: {color};
                background: transparent;
            }}
        """)
    
    def _update_toggle_style(self):
        color = "#8b949e" if self._is_dark else "#656d76"
        hover = "#e6edf3" if self._is_dark else "#1f2328"
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {color};
                font-size: 10px;
            }}
            QPushButton:hover {{
                color: {hover};
            }}
        """)


class CheckboxGroup(QWidget):
    """Group of checkboxes for multi-select filters"""
    
    changed = Signal(list)
    
    def __init__(self, options: List[str], parent=None):
        super().__init__(parent)
        self.checkboxes: Dict[str, QCheckBox] = {}
        self._setup_ui(options)
    
    def _setup_ui(self, options: List[str]):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        for option in options:
            cb = QCheckBox(option)
            cb.setChecked(True)
            cb.setStyleSheet("""
                QCheckBox {
                    color: #8b949e;
                    font-size: 13px;
                    spacing: 8px;
                }
                QCheckBox:hover {
                    color: #e6edf3;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 4px;
                    border: 1px solid #30363d;
                    background: #0d1117;
                }
                QCheckBox::indicator:checked {
                    background: #58a6ff;
                    border-color: #58a6ff;
                }
            """)
            cb.stateChanged.connect(self._on_change)
            self.checkboxes[option] = cb
            layout.addWidget(cb)
    
    def _on_change(self):
        selected = [k for k, v in self.checkboxes.items() if v.isChecked()]
        self.changed.emit(selected)
    
    def get_selected(self) -> List[str]:
        return [k for k, v in self.checkboxes.items() if v.isChecked()]
    
    def select_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(True)
    
    def clear_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(False)
    
    def set_theme(self, is_dark: bool):
        """Update checkbox theme"""
        for cb in self.checkboxes.values():
            if is_dark:
                cb.setStyleSheet("""
                    QCheckBox {
                        color: #8b949e;
                        font-size: 13px;
                        spacing: 8px;
                    }
                    QCheckBox:hover { color: #e6edf3; }
                    QCheckBox::indicator {
                        width: 16px; height: 16px;
                        border-radius: 4px;
                        border: 1px solid #30363d;
                        background: #0d1117;
                    }
                    QCheckBox::indicator:checked {
                        background: #58a6ff;
                        border-color: #58a6ff;
                    }
                """)
            else:
                cb.setStyleSheet("""
                    QCheckBox {
                        color: #656d76;
                        font-size: 13px;
                        spacing: 8px;
                    }
                    QCheckBox:hover { color: #1f2328; }
                    QCheckBox::indicator {
                        width: 16px; height: 16px;
                        border-radius: 4px;
                        border: 1px solid #d0d7de;
                        background: #ffffff;
                    }
                    QCheckBox::indicator:checked {
                        background: #0969da;
                        border-color: #0969da;
                    }
                """)


class RangeSlider(QWidget):
    """Dual-handle range slider"""
    
    changed = Signal(int, int)
    
    def __init__(self, min_val: int, max_val: int, parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Value labels
        labels_layout = QHBoxLayout()
        self.min_label = QLabel(f"${self.min_val}")
        self.min_label.setStyleSheet("color: #58a6ff; font-weight: 600; background: transparent;")
        self.max_label = QLabel(f"${self.max_val}")
        self.max_label.setStyleSheet("color: #58a6ff; font-weight: 600; background: transparent;")
        
        labels_layout.addWidget(self.min_label)
        labels_layout.addStretch()
        labels_layout.addWidget(self.max_label)
        layout.addLayout(labels_layout)
        
        # Min slider
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setRange(self.min_val, self.max_val)
        self.min_slider.setValue(self.min_val)
        self.min_slider.valueChanged.connect(self._on_min_changed)
        layout.addWidget(self.min_slider)
        
        # Max slider
        self.max_slider = QSlider(Qt.Horizontal)
        self.max_slider.setRange(self.min_val, self.max_val)
        self.max_slider.setValue(self.max_val)
        self.max_slider.valueChanged.connect(self._on_max_changed)
        layout.addWidget(self.max_slider)
    
    def _on_min_changed(self, value):
        if value > self.max_slider.value():
            self.min_slider.setValue(self.max_slider.value())
            return
        self.min_label.setText(f"${value}")
        self.changed.emit(value, self.max_slider.value())
    
    def _on_max_changed(self, value):
        if value < self.min_slider.value():
            self.max_slider.setValue(self.min_slider.value())
            return
        self.max_label.setText(f"${value}")
        self.changed.emit(self.min_slider.value(), value)
    
    def get_values(self) -> tuple:
        return self.min_slider.value(), self.max_slider.value()
    
    def set_values(self, min_val: int, max_val: int):
        self.min_slider.setValue(min_val)
        self.max_slider.setValue(max_val)
    
    def set_theme(self, is_dark: bool):
        """Update slider theme"""
        color = "#58a6ff" if is_dark else "#0969da"
        self.min_label.setStyleSheet(f"color: {color}; font-weight: 600; background: transparent;")
        self.max_label.setStyleSheet(f"color: {color}; font-weight: 600; background: transparent;")


class FilterPanel(QWidget):
    """Complete filter panel with all filter controls - matching app_en.py"""
    
    filters_changed = Signal(dict)
    export_requested = Signal()
    borough_changed = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("filterPanel")
        self._is_dark = True
        self._sections = []
        
        # Debounce timer for filter changes
        self._filter_debounce_timer = QTimer()
        self._filter_debounce_timer.setSingleShot(True)
        self._filter_debounce_timer.setInterval(300)  # 300ms debounce
        self._filter_debounce_timer.timeout.connect(self._emit_filters)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._update_panel_style()
        self.setFixedWidth(300)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setObjectName("filterHeader")
        header.setFixedHeight(56)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        self.title = QLabel("🎛️ Filter Panel")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #e6edf3;
            }
        """)
        header_layout.addWidget(self.title)
        
        header_layout.addStretch()
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #58a6ff;
                border: none;
                font-size: 13px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_filters)
        header_layout.addWidget(self.reset_btn)
        
        main_layout.addWidget(header)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setObjectName("filterDivider")
        main_layout.addWidget(divider)
        
        # Active filters display
        self.active_filters_widget = QWidget()
        self.active_filters_widget.setObjectName("activeFilters")
        active_layout = QVBoxLayout(self.active_filters_widget)
        active_layout.setContentsMargins(16, 8, 16, 8)
        
        self.active_filters_label = QLabel("No filters active")
        self.active_filters_label.setWordWrap(True)
        self.active_filters_label.setStyleSheet("font-size: 11px; color: #8b949e;")
        active_layout.addWidget(self.active_filters_label)
        
        main_layout.addWidget(self.active_filters_widget)
        
        # Scroll area for filters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(16)
        
        # 1. Borough / Neighbourhood Group filter
        neighbourhood_section = FilterSection("📍 Borough (Neighbourhood Group)")
        self._sections.append(neighbourhood_section)
        self.neighbourhood_filter = CheckboxGroup([
            "Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"
        ])
        self.neighbourhood_filter.changed.connect(self._on_borough_selection_changed)
        neighbourhood_section.add_widget(self.neighbourhood_filter)
        self.content_layout.addWidget(neighbourhood_section)
        
        # 2. Neighbourhood detail dropdown
        neighbourhood_detail_section = FilterSection("🏘️ Neighbourhood")
        self._sections.append(neighbourhood_detail_section)
        self.neighbourhood_detail_combo = QComboBox()
        self.neighbourhood_detail_combo.addItem("All", "all")
        self.neighbourhood_detail_combo.setStyleSheet(self._get_combo_style())
        self.neighbourhood_detail_combo.currentIndexChanged.connect(self._on_filter_change)
        neighbourhood_detail_section.add_widget(self.neighbourhood_detail_combo)
        self.content_layout.addWidget(neighbourhood_detail_section)
        
        # 3. Room type filter
        room_section = FilterSection("🛏️ Room Type")
        self._sections.append(room_section)
        self.room_filter = CheckboxGroup([
            "Entire home/apt", "Private room", "Shared room"
        ])
        self.room_filter.changed.connect(self._on_filter_change)
        room_section.add_widget(self.room_filter)
        self.content_layout.addWidget(room_section)
        
        # 4. Price range filter
        price_section = FilterSection("💰 Price Range")
        self._sections.append(price_section)
        self.price_filter = ProfessionalRangeSlider(10, 1000, prefix="$")
        self.price_filter.set_values(100, 150)
        self.price_filter.rangeChanged.connect(lambda min_v, max_v: self._on_filter_change())
        price_section.add_widget(self.price_filter)
        self.content_layout.addWidget(price_section)
        
        # 5. Minimum reviews filter
        reviews_section = FilterSection("⭐ Minimum Reviews")
        self._sections.append(reviews_section)
        reviews_layout = QHBoxLayout()
        reviews_layout.setSpacing(8)
        
        self.reviews_input = QSpinBox()
        self.reviews_input.setRange(0, 500)
        self.reviews_input.setValue(0)
        self.reviews_input.setButtonSymbols(QSpinBox.NoButtons)
        self.reviews_input.setAlignment(Qt.AlignCenter)
        self.reviews_input.setPrefix("≥ ")
        self.reviews_input.setSuffix(" reviews")
        self._update_reviews_input_style()
        self.reviews_input.valueChanged.connect(self._on_reviews_input_changed)
        reviews_layout.addWidget(self.reviews_input)
        
        self.reviews_slider = QSlider(Qt.Horizontal)
        self.reviews_slider.setRange(0, 500)
        self.reviews_slider.setValue(0)
        self.reviews_slider.valueChanged.connect(self._on_reviews_slider_changed)
        reviews_layout.addWidget(self.reviews_slider, 3)
        
        reviews_widget = QWidget()
        reviews_widget.setLayout(reviews_layout)
        reviews_section.add_widget(reviews_widget)
        self.content_layout.addWidget(reviews_section)
        
        # 6. Minimum nights filter
        nights_section = FilterSection("📅 Max Stay Requirement")
        self._sections.append(nights_section)
        nights_layout = QHBoxLayout()
        nights_layout.setSpacing(8)
        
        self.nights_input = QSpinBox()
        self.nights_input.setRange(1, 30)
        self.nights_input.setValue(30)
        self.nights_input.setButtonSymbols(QSpinBox.NoButtons)
        self.nights_input.setAlignment(Qt.AlignCenter)
        self.nights_input.setPrefix("≤ ")
        self.nights_input.setSuffix(" nights")
        self._update_nights_input_style()
        self.nights_input.valueChanged.connect(self._on_nights_input_changed)
        nights_layout.addWidget(self.nights_input)
        
        self.nights_slider = QSlider(Qt.Horizontal)
        self.nights_slider.setRange(1, 30)
        self.nights_slider.setValue(30)
        self.nights_slider.valueChanged.connect(self._on_nights_slider_changed)
        nights_layout.addWidget(self.nights_slider, 3)
        
        nights_widget = QWidget()
        nights_widget.setLayout(nights_layout)
        nights_section.add_widget(nights_widget)
        self.content_layout.addWidget(nights_section)
        
        # 7. Host category filter
        host_section = FilterSection("👤 Host Listings Filter")
        self._sections.append(host_section)
        self.host_category_combo = QComboBox()
        self.host_category_combo.addItems([
            "All", "Single (1)", "Small (2-5)", "Medium (6-10)", "Mega (10+)"
        ])
        self.host_category_combo.setStyleSheet(self._get_combo_style())
        self.host_category_combo.currentIndexChanged.connect(self._on_filter_change)
        host_section.add_widget(self.host_category_combo)
        self.content_layout.addWidget(host_section)
        
        # 8. Commercial listing filter
        commercial_section = FilterSection("🏢 Commercial Listing Filter")
        self._sections.append(commercial_section)
        
        self.commercial_checkbox = QCheckBox("Show Only Commercial Listings")
        self.commercial_checkbox.setToolTip("Listings with availability > 300 OR host_listings > 5")
        self.commercial_checkbox.stateChanged.connect(self._on_filter_change)
        self._update_commercial_checkbox_style()
        commercial_section.add_widget(self.commercial_checkbox)
        
        commercial_info = QLabel("ℹ️ Availability > 300 OR Host Listings > 5")
        commercial_info.setStyleSheet("font-size: 10px; color: #8b949e;")
        commercial_info.setWordWrap(True)
        commercial_section.add_widget(commercial_info)
        self.content_layout.addWidget(commercial_section)
        
        # Spacer
        self.content_layout.addStretch()
        
        # Data summary
        summary_section = FilterSection("📊 Data Summary")
        self._sections.append(summary_section)
        self.summary_label = QLabel("Loading...")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("font-size: 12px; color: #8b949e; background: transparent;")
        summary_section.add_widget(self.summary_label)
        self.content_layout.addWidget(summary_section)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)
        
        # Bottom buttons
        button_container = QWidget()
        button_container.setObjectName("filterButtons")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(16, 12, 16, 16)
        button_layout.setSpacing(10)
        
        apply_btn = QPushButton("✓ Apply Filters")
        apply_btn.setCursor(Qt.PointingHandCursor)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        apply_btn.clicked.connect(self._emit_filters)
        button_layout.addWidget(apply_btn)
        
        export_btn = QPushButton("📥 Export")
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #388bfd;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #58a6ff;
            }
        """)
        export_btn.clicked.connect(self._on_export_click)
        button_layout.addWidget(export_btn)
        
        main_layout.addWidget(button_container)
    
    def _get_combo_style(self):
        if self._is_dark:
            return """
                QComboBox {
                    background-color: #0d1117;
                    color: #e6edf3;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 13px;
                }
                QComboBox:hover { border-color: #58a6ff; }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                QComboBox QAbstractItemView {
                    background-color: #161b22;
                    color: #e6edf3;
                    selection-background-color: #388bfd;
                    border: 1px solid #30363d;
                }
            """
        else:
            return """
                QComboBox {
                    background-color: #ffffff;
                    color: #1f2328;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 13px;
                }
                QComboBox:hover { border-color: #0969da; }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #1f2328;
                    selection-background-color: #0969da;
                    border: 1px solid #d0d7de;
                }
            """
    
    def _update_commercial_checkbox_style(self):
        if self._is_dark:
            self.commercial_checkbox.setStyleSheet("""
                QCheckBox {
                    color: #8b949e;
                    font-size: 13px;
                    spacing: 8px;
                }
                QCheckBox:hover { color: #e6edf3; }
                QCheckBox::indicator {
                    width: 16px; height: 16px;
                    border-radius: 4px;
                    border: 1px solid #30363d;
                    background: #0d1117;
                }
                QCheckBox::indicator:checked {
                    background: #f85149;
                    border-color: #f85149;
                }
            """)
        else:
            self.commercial_checkbox.setStyleSheet("""
                QCheckBox {
                    color: #656d76;
                    font-size: 13px;
                    spacing: 8px;
                }
                QCheckBox:hover { color: #1f2328; }
                QCheckBox::indicator {
                    width: 16px; height: 16px;
                    border-radius: 4px;
                    border: 1px solid #d0d7de;
                    background: #ffffff;
                }
                QCheckBox::indicator:checked {
                    background: #cf222e;
                    border-color: #cf222e;
                }
            """)
    
    def _update_reviews_input_style(self):
        """Update reviews input style"""
        if self._is_dark:
            self.reviews_input.setStyleSheet("""
                QSpinBox {
                    background-color: #161b22;
                    color: #58a6ff;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 120px;
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
            self.reviews_input.setStyleSheet("""
                QSpinBox {
                    background-color: #ffffff;
                    color: #0969da;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 120px;
                }
                QSpinBox:focus {
                    border-color: #0969da;
                    background-color: #f6f8fa;
                }
                QSpinBox:hover {
                    border-color: #0969da;
                }
            """)
    
    def _update_nights_input_style(self):
        """Update nights input style"""
        if self._is_dark:
            self.nights_input.setStyleSheet("""
                QSpinBox {
                    background-color: #161b22;
                    color: #58a6ff;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 120px;
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
            self.nights_input.setStyleSheet("""
                QSpinBox {
                    background-color: #ffffff;
                    color: #0969da;
                    border: 1px solid #d0d7de;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 120px;
                }
                QSpinBox:focus {
                    border-color: #0969da;
                    background-color: #f6f8fa;
                }
                QSpinBox:hover {
                    border-color: #0969da;
                }
            """)
    
    def _on_reviews_input_changed(self, value):
        """Handle reviews input change"""
        self.reviews_slider.blockSignals(True)
        self.reviews_slider.setValue(value)
        self.reviews_slider.blockSignals(False)
        self._update_active_filters_display()
    
    def _on_reviews_slider_changed(self, value):
        """Handle reviews slider change"""
        self.reviews_input.blockSignals(True)
        self.reviews_input.setValue(value)
        self.reviews_input.blockSignals(False)
        self._update_active_filters_display()
    
    def _on_nights_input_changed(self, value):
        """Handle nights input change"""
        self.nights_slider.blockSignals(True)
        self.nights_slider.setValue(value)
        self.nights_slider.blockSignals(False)
        self._update_active_filters_display()
    
    def _on_nights_slider_changed(self, value):
        """Handle nights slider change"""
        self.nights_input.blockSignals(True)
        self.nights_input.setValue(value)
        self.nights_input.blockSignals(False)
        self._update_active_filters_display()
    
    def _on_filter_change(self, *args):
        """Handle filter change with debouncing"""
        self._update_active_filters_display()
        # Restart debounce timer
        self._filter_debounce_timer.stop()
        self._filter_debounce_timer.start()
    
    def _emit_filters(self):
        """Emit filters after debounce period"""
        filters = self.get_filters()
        self.filters_changed.emit(filters)
    
    def _update_active_filters_display(self):
        """Update the active filters display"""
        filters = []
        
        # Check neighbourhoods
        selected_boroughs = self.neighbourhood_filter.get_selected()
        if len(selected_boroughs) < 5:
            filters.append(f"📍 {', '.join(selected_boroughs)}")
        
        # Check room types
        selected_rooms = self.room_filter.get_selected()
        if len(selected_rooms) < 3:
            filters.append(f"🛏️ {', '.join(selected_rooms)}")
        
        # Check price
        min_p, max_p = self.price_filter.get_values()
        if min_p > 10 or max_p < 1000:
            filters.append(f"💰 ${min_p}-${max_p}")
        
        # Check reviews
        if self.reviews_input.value() > 0:
            filters.append(f"⭐ ≥{self.reviews_input.value()}")
        
        # Check nights
        if self.nights_input.value() < 30:
            filters.append(f"📅 ≤{self.nights_input.value()} nights")
        
        # Check host category
        if self.host_category_combo.currentIndex() > 0:
            filters.append(f"👤 {self.host_category_combo.currentText()}")
        
        # Check commercial
        if self.commercial_checkbox.isChecked():
            filters.append("🏢 Commercial Only")
        
        if filters:
            self.active_filters_label.setText("Active: " + " | ".join(filters))
            self.active_filters_label.setStyleSheet("font-size: 11px; color: #58a6ff; background: transparent;")
        else:
            self.active_filters_label.setText("No filters active")
            self.active_filters_label.setStyleSheet("font-size: 11px; color: #8b949e; background: transparent;")
    
    def _on_export_click(self):
        """Handle export button click"""
        self.export_requested.emit()
    
    def _on_borough_selection_changed(self, selected: list):
        """Handle borough selection change"""
        self._on_filter_change()
        self.borough_changed.emit(selected)
    
    def set_borough_options(self, boroughs: list):
        """Set available borough options"""
        # Borough filter already has standard boroughs, no need to update
        pass
    
    def set_room_type_options(self, room_types: list):
        """Set available room type options"""
        # Room filter already has standard room types, no need to update
        pass
    
    def set_host_category_options(self, categories: list):
        """Set available host category options"""
        self.host_category_combo.clear()
        self.host_category_combo.addItem("All", "all")
        for cat in categories:
            self.host_category_combo.addItem(cat, cat.lower())
    
    def set_neighbourhood_options(self, neighbourhoods: list):
        """Set available neighbourhood options"""
        self.neighbourhood_detail_combo.blockSignals(True)
        self.neighbourhood_detail_combo.clear()
        self.neighbourhood_detail_combo.addItem("All Neighbourhoods", "all")
        for n in sorted(neighbourhoods):
            self.neighbourhood_detail_combo.addItem(n, n)
        self.neighbourhood_detail_combo.blockSignals(False)
    
    def get_filters(self) -> Dict:
        host_cat = self.host_category_combo.currentText()
        if host_cat == "All":
            host_cat = "all"
        
        neighbourhood_detail = self.neighbourhood_detail_combo.currentData()
        
        return {
            'neighbourhood_group': self.neighbourhood_filter.get_selected(),
            'neighbourhood': neighbourhood_detail,
            'room_type': self.room_filter.get_selected(),
            'price_range': self.price_filter.get_values(),
            'min_nights': self.nights_input.value(),
            'min_reviews': self.reviews_input.value(),
            'host_category': host_cat,
            'commercial_only': self.commercial_checkbox.isChecked()
        }
    
    def reset_filters(self):
        self.neighbourhood_filter.select_all()
        self.neighbourhood_detail_combo.setCurrentIndex(0)
        self.room_filter.select_all()
        self.price_filter.set_values(100, 150)
        self.reviews_input.setValue(0)
        self.reviews_slider.setValue(0)
        self.nights_input.setValue(30)
        self.nights_slider.setValue(30)
        self.host_category_combo.setCurrentIndex(0)
        self.commercial_checkbox.setChecked(False)
        self._update_active_filters_display()
        self._emit_filters()
    
    def update_summary(self, stats: Dict):
        """Update the data summary display"""
        if not stats:
            self.summary_label.setText("No data available")
            return
        
        text = f"""
📊 Total Listings: {stats.get('total_listings', 0):,}
👥 Unique Hosts: {stats.get('total_hosts', 0):,}
💰 Avg Price: ${stats.get('avg_price', 0):.0f}
📈 Median Price: ${stats.get('median_price', 0):.0f}
⭐ Total Reviews: {stats.get('total_reviews', 0):,}
🏢 Commercial: {stats.get('commercial_count', 0):,}
        """.strip()
        self.summary_label.setText(text)
    
    def update_neighbourhoods(self, boroughs: List[str], all_neighbourhoods: Dict[str, List[str]]):
        """Update neighbourhood dropdown based on selected boroughs"""
        self.neighbourhood_detail_combo.blockSignals(True)
        self.neighbourhood_detail_combo.clear()
        self.neighbourhood_detail_combo.addItem("All", "all")
        
        for borough in sorted(boroughs):
            if borough in all_neighbourhoods:
                for n in sorted(all_neighbourhoods[borough]):
                    self.neighbourhood_detail_combo.addItem(f"  {n}", n)
        
        self.neighbourhood_detail_combo.blockSignals(False)
    
    def set_theme(self, is_dark: bool):
        """Update filter panel theme"""
        self._is_dark = is_dark
        self._update_panel_style()
        self.neighbourhood_filter.set_theme(is_dark)
        self.room_filter.set_theme(is_dark)
        self.price_filter.set_theme(is_dark)
        self._update_reviews_input_style()
        self._update_nights_input_style()
        self._update_commercial_checkbox_style()
        
        # Update combo boxes
        self.neighbourhood_detail_combo.setStyleSheet(self._get_combo_style())
        self.host_category_combo.setStyleSheet(self._get_combo_style())
        
        # Update sections
        for section in self._sections:
            section.set_theme(is_dark)
        
        # Update active filters label color
        filter_text_color = "#58a6ff" if is_dark else "#0969da"
        muted_color = "#8b949e" if is_dark else "#656d76"
        
        # Refresh active filters display to update colors
        self._update_active_filters_display()
        
        title_color = "#e6edf3" if is_dark else "#1f2328"
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 15px;
                font-weight: 600;
                color: {title_color};
            }}
        """)
    
    def _update_panel_style(self):
        """Update panel colors based on theme"""
        if self._is_dark:
            self.setStyleSheet("""
                QWidget#filterPanel {
                    background-color: #161b22;
                    border-right: 1px solid #21262d;
                }
                QWidget#filterHeader {
                    background-color: #161b22;
                }
                QFrame#filterDivider {
                    background-color: #21262d;
                }
                QWidget#activeFilters {
                    background-color: #0d1117;
                }
                QWidget#filterButtons {
                    background-color: #161b22;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget#filterPanel {
                    background-color: #ffffff;
                    border-right: 1px solid #d0d7de;
                }
                QWidget#filterHeader {
                    background-color: #f6f8fa;
                }
                QFrame#filterDivider {
                    background-color: #d0d7de;
                }
                QWidget#activeFilters {
                    background-color: #f6f8fa;
                }
                QWidget#filterButtons {
                    background-color: #f6f8fa;
                }
            """)
