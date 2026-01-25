"""
Base View - Abstract base class for all stakeholder views
"""

from abc import abstractmethod
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QSizePolicy, QGridLayout, QSpacerItem
)
from PySide6.QtCore import Qt, Signal
import pandas as pd

from qt_app.widgets.custom_widgets import StatCard, SectionHeader, ModernCard
from qt_app.widgets.charts import PlotlyWidget


class BaseView(QWidget):
    """Base class for all stakeholder views"""
    
    def __init__(self, data_manager, theme_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.theme_manager = theme_manager
        self.charts = []
        self._setup_ui()
        
        # Connect to data changes
        self.data_manager.data_filtered.connect(self.refresh)
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
    
    def _setup_ui(self):
        """Setup the base UI structure"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Content container
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(24)
        
        # View header
        self._setup_header()
        
        # Stats cards row
        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(16)
        self.content_layout.addWidget(self.stats_container)
        
        # Charts section
        self.charts_container = QWidget()
        self.charts_layout = QGridLayout(self.charts_container)
        self.charts_layout.setContentsMargins(0, 0, 0, 0)
        self.charts_layout.setSpacing(16)
        self.content_layout.addWidget(self.charts_container)
        
        # Additional content (to be implemented by subclasses)
        self._setup_content()
        
        self.content_layout.addStretch()
        
        scroll.setWidget(self.content)
        main_layout.addWidget(scroll)
    
    def _setup_header(self):
        """Setup view header with title and description"""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        
        # Persona badge and title row
        title_row = QHBoxLayout()
        
        self.persona_badge = QLabel()
        self.persona_badge.setStyleSheet("""
            QLabel {
                background-color: rgba(88, 166, 255, 0.15);
                color: #58a6ff;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        title_row.addWidget(self.persona_badge)
        title_row.addStretch()
        header_layout.addLayout(title_row)
        
        # Title
        self.title_label = QLabel()
        # Set initial theme colors based on current theme
        is_dark = self.theme_manager.current_theme == 'dark'
        title_color = "#e6edf3" if is_dark else "#1f2328"
        desc_color = "#8b949e" if is_dark else "#656d76"
        
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {title_color};
                background: transparent;
            }}
        """)
        header_layout.addWidget(self.title_label)
        
        # Description
        self.desc_label = QLabel()
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {desc_color};
                line-height: 1.5;
                background: transparent;
            }}
        """)
        header_layout.addWidget(self.desc_label)
        
        self.content_layout.addWidget(header)
    
    @abstractmethod
    def _setup_content(self):
        """Setup view-specific content - to be implemented by subclasses"""
        pass
    
    @abstractmethod
    def refresh(self):
        """Refresh view with new data - to be implemented by subclasses"""
        pass
    
    def _on_theme_changed(self, theme: str):
        """Handle theme change"""
        is_dark = theme == 'dark'
        self._update_view_theme(is_dark)
        # Refresh the entire view to redraw charts with new theme
        self.refresh()
    
    def _update_view_theme(self, is_dark: bool):
        """Update view colors based on theme"""
        title_color = "#e6edf3" if is_dark else "#1f2328"
        desc_color = "#8b949e" if is_dark else "#656d76"
        badge_bg = "rgba(88, 166, 255, 0.15)" if is_dark else "#ddf4ff"
        badge_text = "#58a6ff" if is_dark else "#0969da"
        
        self.title_label.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {title_color}; background: transparent;")
        
        self.desc_label.setStyleSheet(f"font-size: 14px; color: {desc_color}; line-height: 1.5; background: transparent;")
        
        self.persona_badge.setStyleSheet(f"background-color: {badge_bg}; color: {badge_text}; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500;")
        
        # Update all info cards in the view
        self._update_info_cards_theme(is_dark)
        
        # Update stat cards
        self._update_stat_cards_theme(is_dark)
    
    def _update_info_cards_theme(self, is_dark: bool):
        """Update info card colors based on theme"""
        title_color = "#e6edf3" if is_dark else "#1f2328"
        content_color = "#8b949e" if is_dark else "#656d76"
        card_bg = "#161b22" if is_dark else "#ffffff"
        card_border = "#30363d" if is_dark else "#d0d7de"
        
        # Find all ModernCards with title_label and content_label
        for card in self.findChildren(ModernCard):
            # Update card background
            card.setStyleSheet(f"""
                ModernCard {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-radius: 12px;
                }}
            """)
            
            # Update title and content labels if they exist
            if hasattr(card, 'title_label') and hasattr(card, 'content_label'):
                card.title_label.setStyleSheet(f"""
                    font-size: 14px;
                    font-weight: 600;
                    color: {title_color};
                    background: transparent;
                """)
                card.content_label.setStyleSheet(f"""
                    font-size: 13px;
                    color: {content_color};
                    line-height: 1.6;
                    background: transparent;
                """)
            
            # Update other labels with specific object names
            for label in card.findChildren(QLabel):
                obj_name = label.objectName()
                if obj_name == "info_card_title" or "title" in obj_name.lower():
                    label.setStyleSheet(f"""
                        font-size: 14px;
                        font-weight: 600;
                        color: {title_color};
                        background: transparent;
                    """)
                elif obj_name == "info_card_content" or "content" in obj_name.lower():
                    label.setStyleSheet(f"""
                        font-size: 13px;
                        color: {content_color};
                        line-height: 1.6;
                        background: transparent;
                    """)
    
    def _update_stat_cards_theme(self, is_dark: bool):
        """Update stat card labels based on theme"""
        label_color = "#8b949e" if is_dark else "#656d76"
        card_bg = "#161b22" if is_dark else "#ffffff"
        card_border = "#30363d" if is_dark else "#d0d7de"
        
        for card in self.findChildren(StatCard):
            # Update the muted label color (third child)
            for child in card.findChildren(QLabel):
                if child.property("class") == "muted":
                    child.setStyleSheet(f"font-size: 13px; color: {label_color};")
            
            # Update card background
            card.setStyleSheet(f"""
                StatCard {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-radius: 12px;
                }}
            """)
    
    def add_stat_card(self, icon: str, value: str, label: str, color: str = "#58a6ff") -> StatCard:
        """Add a stat card to the stats row"""
        card = StatCard(icon, value, label, color)
        self.stats_layout.addWidget(card)
        return card
    
    def add_chart(self, row: int, col: int, row_span: int = 1, col_span: int = 1) -> PlotlyWidget:
        """Add a chart widget at specified grid position"""
        chart = PlotlyWidget()
        chart.setMinimumHeight(800)  # Minimum height to ensure visibility
        self.charts_layout.addWidget(chart, row, col, row_span, col_span)
        self.charts.append(chart)
        return chart
    
    def create_info_card(self, title: str, content: str) -> ModernCard:
        """Create an info card with title and content"""
        card = ModernCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        is_dark = self.theme_manager.current_theme == 'dark'
        title_color = "#e6edf3" if is_dark else "#1f2328"
        content_color = "#8b949e" if is_dark else "#656d76"
        
        title_label = QLabel(title)
        title_label.setObjectName("info_card_title")
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {title_color};
            background: transparent;
        """)
        layout.addWidget(title_label)
        
        content_label = QLabel(content)
        content_label.setObjectName("info_card_content")
        content_label.setWordWrap(True)
        content_label.setStyleSheet(f"""
            font-size: 13px;
            color: {content_color};
            line-height: 1.6;
            background: transparent;
        """)
        layout.addWidget(content_label)
        
        # Store reference for theme updates
        card.title_label = title_label
        card.content_label = content_label
        
        return card
    
    def add_data_quality_indicators(self):
        """Add data quality and missing data indicators to the view"""
        from qt_app.widgets.custom_widgets import DataQualityBadge, MissingDataBadge
        
        # Get data quality info
        quality_info = self.data_manager.get_data_quality_score()
        missing_info = self.data_manager.get_missing_data_stats()
        
        # Create indicators container
        indicators_container = QWidget()
        indicators_layout = QHBoxLayout(indicators_container)
        indicators_layout.setContentsMargins(0, 0, 0, 0)
        indicators_layout.setSpacing(8)
        
        # Add data quality badge
        if quality_info and 'score' in quality_info:
            quality_badge = DataQualityBadge(quality_info['score'])
            indicators_layout.addWidget(quality_badge)
        
        # Add missing data badges
        if missing_info:
            for col, stats in missing_info.items():
                badge = MissingDataBadge(
                    stats['count'], 
                    stats['percentage'], 
                    col.replace('_', ' ').title()
                )
                indicators_layout.addWidget(badge)
        
        indicators_layout.addStretch()
        self.content_layout.addWidget(indicators_container)
