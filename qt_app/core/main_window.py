"""
Main Window - Central application window with navigation and content areas
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QPushButton, QSplitter, QFrame, QStatusBar, QMessageBox,
    QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QShortcut, QKeySequence, QIcon

from qt_app.widgets.sidebar import ModernSidebar
from qt_app.widgets.filter_panel import FilterPanel
from qt_app.widgets.custom_widgets import LoadingSpinner
from qt_app.core.data_manager import DataManager
from qt_app.core.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, theme_manager: ThemeManager):
        super().__init__()
        self.theme_manager = theme_manager
        self.data_manager = DataManager()
        self.views = {}
        
        self._setup_window()
        self._setup_ui()
        self._setup_shortcuts()
        self._connect_signals()
        self._load_data()
    
    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("NYC Airbnb Dashboard - Modern Analytics Platform")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar navigation
        self.sidebar = ModernSidebar()
        self._setup_navigation()
        main_layout.addWidget(self.sidebar)
        
        # Content area with filter panel
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Filter panel
        self.filter_panel = FilterPanel()
        content_layout.addWidget(self.filter_panel)
        
        # Main content area
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #0d1117;")
        content_area_layout = QVBoxLayout(content_area)
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        content_area_layout.setSpacing(0)
        
        # Top bar
        self._setup_top_bar(content_area_layout)
        
        # Stacked widget for views
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #0d1117;")
        content_area_layout.addWidget(self.stack, 1)
        
        # Loading overlay
        self._setup_loading_overlay()
        
        content_layout.addWidget(content_area, 1)
        main_layout.addWidget(content_container, 1)
        
        # Status bar
        self._setup_status_bar()
    
    def _setup_navigation(self):
        """Setup sidebar navigation items"""
        # Main views section
        main_section = self.sidebar.add_section("Perspectives")
        
        self.sidebar.add_nav_item(main_section, "🧳", "Traveler", "traveler")
        self.sidebar.add_nav_item(main_section, "🏠", "Investor", "investor")
        self.sidebar.add_nav_item(main_section, "📋", "Regulator", "regulator")
        self.sidebar.add_nav_item(main_section, "🏨", "Competitor", "competitor")
        self.sidebar.add_nav_item(main_section, "📰", "Journalist", "journalist")
        
        self.sidebar.add_spacer()
        
        # Tools section
        tools_section = self.sidebar.add_section("Tools")
        self.sidebar.add_nav_item(tools_section, "📤", "Export Data", "export")
        self.sidebar.add_nav_item(tools_section, "⚙️", "Settings", "settings")
        self.sidebar.add_nav_item(tools_section, "❓", "Help", "help")
        
        # Set default view
        self.sidebar.set_active("traveler")
    
    def _setup_top_bar(self, parent_layout):
        """Setup top toolbar"""
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(56)
        self.top_bar.setStyleSheet("""
            QWidget {
                background-color: #161b22;
                border-bottom: 1px solid #21262d;
            }
        """)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # View title
        self.view_title = QLabel("Dashboard")
        self.view_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #e6edf3;
            }
        """)
        layout.addWidget(self.view_title)
        
        layout.addStretch()
        
        # Stats summary
        self.stats_label = QLabel("Loading data...")
        self.stats_label.setStyleSheet("color: #8b949e; font-size: 13px;")
        layout.addWidget(self.stats_label)
        
        layout.addSpacing(20)
        
        # Action buttons
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #30363d;
            }
        """)
        refresh_btn.clicked.connect(self._refresh_current_view)
        layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📤 Export")
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        export_btn.clicked.connect(self._export_data)
        layout.addWidget(export_btn)
        
        parent_layout.addWidget(self.top_bar)
    
    def _setup_loading_overlay(self):
        """Setup loading overlay"""
        self.loading_overlay = QWidget(self.stack)
        self.loading_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(13, 17, 23, 0.9);
            }
        """)
        
        overlay_layout = QVBoxLayout(self.loading_overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)
        
        self.spinner = LoadingSpinner(60)
        overlay_layout.addWidget(self.spinner, alignment=Qt.AlignCenter)
        
        loading_label = QLabel("Loading data...")
        loading_label.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 16px;
                margin-top: 16px;
            }
        """)
        overlay_layout.addWidget(loading_label, alignment=Qt.AlignCenter)
        
        self.loading_overlay.hide()
    
    def _setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #161b22;
                border-top: 1px solid #21262d;
                color: #8b949e;
                padding: 4px 12px;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Navigation shortcuts
        QShortcut(QKeySequence("1"), self, lambda: self._navigate_to("traveler"))
        QShortcut(QKeySequence("2"), self, lambda: self._navigate_to("investor"))
        QShortcut(QKeySequence("3"), self, lambda: self._navigate_to("regulator"))
        QShortcut(QKeySequence("4"), self, lambda: self._navigate_to("competitor"))
        QShortcut(QKeySequence("5"), self, lambda: self._navigate_to("journalist"))
        
        # Action shortcuts
        QShortcut(QKeySequence("Ctrl+R"), self, self._refresh_current_view)
        QShortcut(QKeySequence("Ctrl+E"), self, self._export_data)
        QShortcut(QKeySequence("Ctrl+D"), self, self._toggle_theme)
        QShortcut(QKeySequence("Ctrl+G"), self, self._toggle_grayscale)  # New: Grayscale mode
        QShortcut(QKeySequence("F11"), self, self._toggle_fullscreen)
        QShortcut(QKeySequence("?"), self, self._show_help)
        QShortcut(QKeySequence("Escape"), self, self._handle_escape)
    
    def _connect_signals(self):
        """Connect all signals"""
        self.sidebar.navigation_changed.connect(self._on_navigation_changed)
        self.sidebar.theme_toggle.toggled.connect(self._on_theme_toggle)
        self.sidebar.grayscale_toggle.toggled.connect(self._on_grayscale_toggle)
        self.filter_panel.filters_changed.connect(self._on_filters_changed)
        self.filter_panel.export_requested.connect(self._export_data)
        self.data_manager.data_loaded.connect(self._on_data_loaded)
        self.data_manager.data_filtered.connect(self._on_data_filtered)
        self.data_manager.filters_resulted_empty.connect(self._on_filters_empty)
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
    
    def _load_data(self):
        """Load the dataset"""
        self.show_loading(True)
        self.status_bar.showMessage("Loading dataset...")
        
        # Get the data file path - go up two levels from core folder to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))  # core/
        qt_app_dir = os.path.dirname(current_dir)  # qt_app/
        project_dir = os.path.dirname(qt_app_dir)  # Project - Copy/
        data_path = os.path.join(project_dir, 'AB_NYC_2019.csv')
        
        # Load data synchronously for now
        QTimer.singleShot(100, lambda: self._do_load_data(data_path))
    
    def _do_load_data(self, path):
        """Actually load the data"""
        try:
            self.data_manager.load_data_sync(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.show_loading(False)
    
    def _on_data_loaded(self):
        """Handle data loaded event"""
        self.show_loading(False)
        self._setup_views()
        self._update_stats_label()
        self.status_bar.showMessage(f"Loaded {len(self.data_manager.df):,} listings")
        
        # Setup filter panel with data
        self._setup_filter_panel_data()
        
        # Show first view
        self._navigate_to("traveler")
    
    def _setup_filter_panel_data(self):
        """Setup filter panel with actual data values"""
        if self.data_manager.df is None:
            return
        
        # Get unique values for dropdowns
        boroughs = sorted(self.data_manager.df['neighbourhood_group'].unique().tolist())
        room_types = sorted(self.data_manager.df['room_type'].unique().tolist())
        
        # Get host categories if available
        host_categories = self.data_manager.get_host_categories()
        
        # Update filter panel
        self.filter_panel.set_borough_options(boroughs)
        self.filter_panel.set_room_type_options(room_types)
        self.filter_panel.set_host_category_options(host_categories)
        
        # Connect borough change to update neighbourhoods
        self.filter_panel.borough_changed.connect(self._on_borough_changed)
    
    def _on_borough_changed(self, boroughs: list):
        """Update neighbourhood dropdown when borough selection changes"""
        neighbourhoods = self.data_manager.get_neighbourhoods_for_borough(boroughs)
        self.filter_panel.set_neighbourhood_options(neighbourhoods)
    
    def _setup_views(self):
        """Setup views with lazy loading for better performance"""
        # Views will be created on-demand when first accessed
        self.views = {}
        self._view_classes = {
            'traveler': 'qt_app.views.traveler_view.TravelerView',
            'investor': 'qt_app.views.investor_view.InvestorView',
            'regulator': 'qt_app.views.regulator_view.RegulatorView',
            'competitor': 'qt_app.views.competitor_view.CompetitorView',
            'journalist': 'qt_app.views.journalist_view.JournalistView',
        }
    
    def _get_or_create_view(self, key: str):
        """Get existing view or create it on-demand (lazy loading)"""
        if key not in self.views:
            # Import and create view only when needed
            module_path, class_name = self._view_classes[key].rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            view_class = getattr(module, class_name)
            
            # Create and add to stack
            view = view_class(self.data_manager, self.theme_manager)
            self.views[key] = view
            self.stack.addWidget(view)
            
            # Initial refresh for new view
            view.refresh()
        
        return self.views[key]
    
    def _get_or_create_view(self, key: str):
        """Get existing view or create it on-demand (lazy loading)"""
        if key not in self.views:
            # Import and create view only when needed
            module_path, class_name = self._view_classes[key].rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            view_class = getattr(module, class_name)
            
            # Create and add to stack
            view = view_class(self.data_manager, self.theme_manager)
            self.views[key] = view
            self.stack.addWidget(view)
            
            # Initial refresh for new view
            view.refresh()
        
        return self.views[key]
    
    def _on_navigation_changed(self, key: str):
        """Handle navigation change"""
        if key in ['export', 'settings', 'help']:
            self._handle_action(key)
            return
        
        self._navigate_to(key)
    
    def _navigate_to(self, key: str):
        """Navigate to a specific view"""
        if key not in self._view_classes:
            return
        
        view = self._get_or_create_view(key)
        self.stack.setCurrentWidget(view)
        self.sidebar.set_active(key)
        
        # Update title
        titles = {
            'traveler': '🧳 Traveler View',
            'investor': '🏠 Investor View', 
            'regulator': '📋 Regulator View',
            'competitor': '🏨 Competitor View',
            'journalist': '📰 Journalist View'
        }
        self.view_title.setText(titles.get(key, 'Dashboard'))
        
        self.status_bar.showMessage(f"Viewing: {key.title()} perspective")
    
    def _handle_action(self, action: str):
        """Handle action navigation items"""
        if action == 'export':
            self._export_data()
        elif action == 'settings':
            self._show_settings()
        elif action == 'help':
            self._show_help()
    
    def _on_filters_changed(self, filters: dict):
        """Handle filter changes"""
        self.show_loading(True)
        self.status_bar.showMessage("Applying filters...")
        
        QTimer.singleShot(50, lambda: self._apply_filters(filters))
    
    def _apply_filters(self, filters: dict):
        """Apply filters to data"""
        self.data_manager.apply_filters(filters)
    
    def _on_data_filtered(self):
        """Handle data filtered event"""
        self.show_loading(False)
        self._update_stats_label()
        
        filtered_count = len(self.data_manager.filtered_df)
        total_count = len(self.data_manager.df)
        self.status_bar.showMessage(f"Showing {filtered_count:,} of {total_count:,} listings")
        
        # Refresh the current view with filtered data
        current_view = self.stack.currentWidget()
        if current_view and hasattr(current_view, 'refresh'):
            current_view.refresh()
    
    def _on_filters_empty(self):
        """Handle empty filter result"""
        self.show_loading(False)
        
        QMessageBox.warning(
            self,
            "No Results Found",
            "The selected filters did not return any results.\n\n"
            "The previous filter results are still displayed.\n"
            "Please adjust your filter criteria and try again."
        )
        
        self.status_bar.showMessage("No results found - keeping previous filter")
    
    def _update_stats_label(self):
        """Update the stats summary label"""
        if self.data_manager.filtered_df is None:
            return
        
        stats = self.data_manager.get_stats()
        self.stats_label.setText(
            f"📊 {stats['total_listings']:,} listings | "
            f"💰 Avg ${stats['avg_price']:.0f} | "
            f"👥 {stats['total_hosts']:,} hosts"
        )
                
        # Update filter panel data summary
        self.filter_panel.update_summary(stats)
    
    
    def _on_theme_toggle(self, is_dark: bool):
        """Handle theme toggle"""
        theme = 'dark' if is_dark else 'light'
        # Just apply theme - this will emit theme_changed signal
        # and _on_theme_changed will handle the rest
        self.theme_manager.apply_theme(QApplication.instance(), theme)
    
    def _update_top_bar_theme(self, is_dark: bool):
        """Update top bar colors"""
        if is_dark:
            self.top_bar.setStyleSheet("""
                QWidget {
                    background-color: #161b22;
                    border-bottom: 1px solid #21262d;
                }
            """)
            self.view_title.setStyleSheet("QLabel { font-size: 18px; font-weight: 600; color: #e6edf3; }")
            self.stats_label.setStyleSheet("color: #8b949e; font-size: 13px;")
        else:
            self.top_bar.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border-bottom: 1px solid #d0d7de;
                }
            """)
            self.view_title.setStyleSheet("QLabel { font-size: 18px; font-weight: 600; color: #1f2328; }")
            self.stats_label.setStyleSheet("color: #656d76; font-size: 13px;")
    
    def _update_content_theme(self, is_dark: bool):
        """Update content area theme"""
        bg_color = "#0d1117" if is_dark else "#f6f8fa"
        self.stack.setStyleSheet(f"background-color: {bg_color};")
    
    def _on_grayscale_toggle(self, enabled: bool):
        """Handle grayscale toggle from sidebar"""
        self.theme_manager.toggle_grayscale_mode()
        
        # Update status bar
        mode_text = "ON" if enabled else "OFF"
        self.status_bar.showMessage(f"Grayscale Mode: {mode_text}", 2000)
        
        # Refresh current view to update colors
        current_view = self.stack.currentWidget()
        if current_view and hasattr(current_view, 'refresh'):
            current_view.refresh()
    
    def _on_theme_changed(self, theme: str):
        """Handle theme change from theme manager"""
        is_dark = theme == 'dark'
        
        # Update sidebar toggle (block signals to avoid recursion)
        self.sidebar.theme_toggle.blockSignals(True)
        self.sidebar.theme_toggle.setChecked(is_dark)
        self.sidebar.theme_toggle.blockSignals(False)
        
        # Update all UI components with new theme
        self.sidebar.set_theme(is_dark)
        self.filter_panel.set_theme(is_dark)
        self._update_top_bar_theme(is_dark)
        self._update_content_theme(is_dark)
        
        # Only refresh the currently visible view for better performance
        # Other views will update when they become visible (via their theme_changed signal)
        current_view = self.stack.currentWidget()
        if current_view and hasattr(current_view, 'refresh'):
            current_view.refresh()
    
    def _toggle_theme(self):
        """Toggle between dark and light themes"""
        self.sidebar.theme_toggle.toggle()
    
    def _refresh_current_view(self):
        """Refresh the current view"""
        current = self.stack.currentWidget()
        if current and hasattr(current, 'refresh'):
            self.show_loading(True)
            QTimer.singleShot(50, lambda: self._do_refresh(current))
    
    def _do_refresh(self, view):
        """Actually refresh the view"""
        view.refresh()
        self.show_loading(False)
        self.status_bar.showMessage("View refreshed")
    
    def _export_data(self):
        """Export filtered data to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "airbnb_data.csv", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                self.data_manager.export_to_csv(file_path)
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def _show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", 
            "Settings panel coming soon!\n\n"
            "Current shortcuts:\n"
            "• 1-5: Switch views\n"
            "• Ctrl+D: Toggle theme\n"
            "• Ctrl+R: Refresh\n"
            "• Ctrl+E: Export\n"
            "• F11: Fullscreen\n"
            "• ?: Help"
        )
    
    def _show_help(self):
        """Show help dialog"""
        QMessageBox.information(self, "Help - NYC Airbnb Dashboard",
            "🏠 NYC Airbnb Dashboard v2.0\n\n"
            "A modern data visualization platform for analyzing\n"
            "NYC Airbnb listings from 5 different perspectives.\n\n"
            "📊 Views:\n"
            "• Traveler: Find affordable accommodations\n"
            "• Investor: Analyze investment opportunities\n"
            "• Regulator: Monitor compliance issues\n"
            "• Competitor: Hotel industry analysis\n"
            "• Journalist: Discover data stories\n\n"
            "⌨️ Keyboard Shortcuts:\n"
            "1-5: Switch between views\n"
            "Ctrl+D: Toggle dark/light mode\n"
            "Ctrl+G: Toggle grayscale mode (accessibility)\n"
            "Ctrl+R: Refresh current view\n"
            "Ctrl+E: Export filtered data\n"
            "F11: Toggle fullscreen\n"
            "Escape: Exit fullscreen\n\n"
            "📁 Data: Inside Airbnb NYC 2019"
        )
    
    def _toggle_grayscale(self):
        """Toggle grayscale mode for accessibility testing"""
        enabled = self.theme_manager.toggle_grayscale_mode()
        mode_text = "Enabled" if enabled else "Disabled"
        self.status_bar.showMessage(f"Grayscale mode {mode_text}", 3000)
        # Refresh current view to apply changes
        self._refresh_current_view()
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def _handle_escape(self):
        """Handle escape key"""
        if self.isFullScreen():
            self.showNormal()
    
    def show_loading(self, show: bool):
        """Show or hide loading overlay"""
        if show:
            self.loading_overlay.setGeometry(self.stack.rect())
            self.loading_overlay.raise_()
            self.loading_overlay.show()
            self.spinner.start()
        else:
            self.loading_overlay.hide()
            self.spinner.stop()
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.setGeometry(self.stack.rect())
