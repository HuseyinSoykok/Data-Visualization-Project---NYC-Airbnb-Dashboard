# 🏠 NYC Airbnb Dashboard - Modern PySide6 Edition

A professional, modern desktop application for analyzing NYC Airbnb data with an intuitive user interface built on PySide6/Qt6.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎨 Modern UI/UX
- **Dark/Light Theme**: Smooth theme switching with modern color palettes
- **Responsive Design**: Adapts to different screen sizes
- **Smooth Animations**: Fade, slide, and pulse effects for better UX
- **Collapsible Sidebar**: Space-efficient navigation
- **Loading States**: Visual feedback during data operations

### 📊 5 Stakeholder Perspectives

1. **🧳 Traveler View** (Hüseyin)
   - Find affordable accommodations
   - Compare prices across boroughs
   - Discover budget-friendly options

2. **🏠 Investor View** (David)
   - Analyze investment opportunities
   - Revenue projections
   - Market saturation analysis

3. **📋 Regulator View** (Dr. Chen)
   - Monitor compliance issues
   - Identify potential violations
   - Policy impact analysis

4. **🏨 Competitor View** (Maria)
   - Hotel industry competitive analysis
   - Market positioning insights
   - Pricing strategy comparison

5. **📰 Journalist View** (Michael)
   - Discover data stories
   - Market inequality analysis
   - Trend exploration

### 🛠️ Technical Features
- **Plotly Integration**: Interactive charts via WebEngine
- **Real-time Filtering**: Dynamic data filtering
- **Export Functionality**: Export filtered data to CSV
- **Keyboard Shortcuts**: Power-user navigation
- **Performance Optimized**: Efficient data handling

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd "d:\Data Visualization\Project - Copy"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r qt_app/requirements.txt
   ```

4. **Run the application:**
   ```bash
   python -m qt_app.main
   ```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `1-5` | Switch between views |
| `Ctrl+D` | Toggle dark/light mode |
| `Ctrl+R` | Refresh current view |
| `Ctrl+E` | Export data |
| `F11` | Toggle fullscreen |
| `Escape` | Exit fullscreen |
| `?` | Show help |

## 📁 Project Structure

```
qt_app/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── core/
│   ├── main_window.py     # Main application window
│   ├── theme_manager.py   # Dark/Light theme handling
│   ├── data_manager.py    # Data loading and filtering
│   └── animations.py      # Animation utilities
├── widgets/
│   ├── custom_widgets.py  # Modern UI components
│   ├── sidebar.py         # Navigation sidebar
│   ├── filter_panel.py    # Data filters
│   └── charts.py          # Plotly chart widgets
└── views/
    ├── base_view.py       # Base view class
    ├── traveler_view.py   # Traveler perspective
    ├── investor_view.py   # Investor perspective
    ├── regulator_view.py  # Regulator perspective
    ├── competitor_view.py # Competitor perspective
    └── journalist_view.py # Journalist perspective
```

## 🎨 Design Principles

- **GitHub-inspired Dark Theme**: Modern, easy on the eyes
- **Consistent Spacing**: 8px grid system
- **Typography Hierarchy**: Clear visual hierarchy
- **Accessible Colors**: WCAG-compliant contrast ratios
- **Micro-interactions**: Subtle hover and click feedback

## 📊 Data Source

This dashboard uses the Inside Airbnb NYC 2019 dataset (`AB_NYC_2019.csv`), containing:
- ~49,000 Airbnb listings
- 16 data fields including price, location, reviews
- 5 NYC boroughs coverage

## 🔧 Configuration

### Theme Customization
Edit `core/theme_manager.py` to customize colors:

```python
THEMES = {
    'dark': {
        'bg_primary': '#0d1117',
        'accent': '#58a6ff',
        # ... more colors
    }
}
```

### Adding New Views
1. Create a new view file in `views/`
2. Extend `BaseView` class
3. Implement `_setup_content()` and `refresh()` methods
4. Register in `MainWindow._setup_views()`

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🙏 Acknowledgments

- Inside Airbnb for the open dataset
- Qt/PySide6 community
- Plotly for interactive visualizations
