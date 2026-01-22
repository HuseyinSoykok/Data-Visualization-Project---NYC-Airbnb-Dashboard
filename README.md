# 🏠 NYC Airbnb Dashboard - Modern PySide6 Edition

A professional, modern desktop application for analyzing NYC Airbnb data with an intuitive user interface built on PySide6/Qt6.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Running the Application](#-running-the-application)
- [User Guide](#-user-guide)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Project Structure](#-project-structure)

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
- **Real-time Filtering**: Dynamic data filtering with instant updates
- **Export Functionality**: Export filtered data to CSV
- **Keyboard Shortcuts**: Power-user navigation
- **Performance Optimized**: Lazy loading, GPU acceleration, efficient data handling

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **CPU**: Intel Core i3 or equivalent
- **RAM**: 4 GB
- **Display**: 1280x720 resolution
- **Python**: 3.10 or higher
- **Internet**: Required for map tiles only

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 22.04+)
- **CPU**: Intel Core i5 or equivalent
- **RAM**: 8 GB or more
- **Display**: 1920x1080 resolution or higher
- **Python**: 3.11 or 3.12
- **GPU**: Integrated graphics with WebGL support

## 🚀 Installation Guide

### Step 1: Check Python Installation

First, verify that Python 3.10 or higher is installed:

```bash
python --version
```

If Python is not installed or version is below 3.10, download from [python.org](https://www.python.org/downloads/)

**Important for Windows users**: During installation, check ✅ "Add Python to PATH"

### Step 2: Clone the Repository

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/HuseyinSoykok/Data-Visualization-Project---NYC-Airbnb-Dashboard.git
cd Data-Visualization-Project---NYC-Airbnb-Dashboard
```

**Option B: Download ZIP**
1. Go to [GitHub Repository](https://github.com/HuseyinSoykok/Data-Visualization-Project---NYC-Airbnb-Dashboard)
2. Click green "Code" button → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in extracted folder

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv_qt
venv_qt\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv_qt
source venv_qt/bin/activate
```

✅ You should see `(venv_qt)` at the beginning of your terminal prompt

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r qt_app/requirements.txt
```

⏱️ This may take 2-5 minutes depending on your internet speed.

### Step 5: Verify Installation

Check if all packages are installed correctly:

```bash
pip list
```

You should see:
- PySide6 (6.10.1 or higher)
- plotly (5.24.1 or higher)
- pandas (2.2.3 or higher)

## 🎮 Running the Application

### First Time Launch

1. Make sure virtual environment is activated (you should see `(venv_qt)`)
2. Run the application:

```bash
python -m qt_app.main
```

3. Wait 5-10 seconds for initial data loading
4. The dashboard window should appear

### Successful Launch

You should see:
```
Loading data from AB_NYC_2019.csv...
Data loaded successfully: 48895 rows
Applying filters...
Starting Qt application...
```

### Subsequent Launches

Same command every time:
```bash
# Activate virtual environment first
venv_qt\Scripts\activate          # Windows
source venv_qt/bin/activate       # macOS/Linux

# Run application
python -m qt_app.main
```

## 📖 User Guide

### Navigation

**Sidebar Menu (Left)**
- Click on any persona icon to switch views
- Each view shows data from that stakeholder's perspective
- Current view is highlighted

**Theme Toggle (Top Right)**
- 🌙 Dark Mode (default)
- ☀️ Light Mode
- Click icon to toggle

**Filter Panel (Right)**
- Expand/collapse using the arrow button
- All filters apply across all views
- Changes update visualizations instantly

### Using Filters

#### Borough Selection
- ✅ Check boxes to include boroughs
- 🔲 Uncheck to exclude
- Default: All boroughs selected

#### Price Range
- Drag sliders to set min/max price
- Or type exact values in input boxes
- Range: $0 - $10,000 per night

#### Room Type
- Entire home/apt: Full property
- Private room: Private room in shared property
- Shared room: Shared sleeping space

#### Reviews Filter
- Set minimum number of reviews
- Higher = More established listings
- 0 = Show all listings

#### Minimum Nights
- Filter by minimum stay requirement
- Lower values = Short-term rentals
- Higher values = Long-term rentals

#### Host Categories
- Single: 1 listing
- Small: 2-5 listings
- Medium: 6-10 listings
- Mega: 10+ listings (professional hosts)

#### Commercial Filter
- Toggle to show only commercial operations
- Commercial = High availability (>300 days) or many listings (>5)

### Interacting with Charts

**All Charts Support:**
- 🖱️ **Hover**: See detailed information
- 🔍 **Zoom**: Click and drag to zoom area
- 📍 **Pan**: Hold Shift + drag to pan
- 🔄 **Reset**: Double-click to reset view
- 💾 **Export**: Click camera icon to save as PNG

**Map Charts:**
- Zoom: Scroll wheel or +/- buttons
- Pan: Click and drag
- Click markers for listing details

**Bar/Line Charts:**
- Hover for exact values
- Click legend items to show/hide data

### Exporting Data

1. Apply filters to your dataset
2. Press `Ctrl+E` or use File → Export menu
3. Choose save location
4. Data saves as CSV with current filters applied

### Refreshing Data

- Press `Ctrl+R` or click 🔄 button
- Reloads data with current filters
- Use after changing external data file

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `1` | Switch to Traveler View |
| `2` | Switch to Investor View |
| `3` | Switch to Regulator View |
| `4` | Switch to Competitor View |
| `5` | Switch to Journalist View |
| `Ctrl+D` | Toggle Dark/Light mode |
| `Ctrl+R` | Refresh current view |
| `Ctrl+E` | Export filtered data |
| `Ctrl+F` | Toggle filter panel |
| `F11` | Toggle fullscreen |
| `Escape` | Exit fullscreen |
| `Ctrl+Q` | Quit application |
| `?` | Show help dialog |

## 🔧 Troubleshooting

### Issue: "Python is not recognized as an internal or external command"

**Solution:**
1. Reinstall Python from [python.org](https://www.python.org/downloads/)
2. During installation, check ✅ "Add Python to PATH"
3. Restart your terminal

### Issue: "ModuleNotFoundError: No module named 'PySide6'"

**Solution:**
```bash
# Make sure virtual environment is activated
venv_qt\Scripts\activate  # Windows
source venv_qt/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r qt_app/requirements.txt
```

### Issue: "FileNotFoundError: AB_NYC_2019.csv not found"

**Solution:**
- Check that `AB_NYC_2019.csv` is in the project root folder
- File should be at the same level as `qt_app/` folder
- If missing, download from [Inside Airbnb](http://insideairbnb.com/get-the-data.html)

### Issue: Application window is blank or white

**Solution:**
1. Update graphics drivers
2. Try disabling GPU acceleration in `qt_app/widgets/charts.py`:
   ```python
   # Set to False
   settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, False)
   ```
3. Restart application

### Issue: Charts not loading or showing errors

**Solution:**
1. Clear browser cache:
   ```bash
   # Delete this folder if it exists
   rm -rf ~/.cache/QtWebEngine  # Linux/Mac
   del /s /q %LOCALAPPDATA%\QtWebEngine  # Windows
   ```
2. Restart application

### Issue: Slow performance with filters

**Solution:**
- Reduce price range to narrow dataset
- Select fewer boroughs
- Close other applications to free RAM
- On older computers, avoid applying all filters at once

### Issue: "Permission denied" when running

**macOS/Linux Solution:**
```bash
chmod +x qt_app/main.py
python -m qt_app.main
```

**Windows Solution:**
- Right-click → "Run as Administrator"

## ❓ FAQ

### Q: Do I need an internet connection?

**A:** No for most features. Internet is only needed for:
- Map tile loading (first time)
- After that, tiles are cached locally

### Q: Can I use my own data?

**A:** Yes! Replace `AB_NYC_2019.csv` with your own CSV file. Required columns:
- `id`, `name`, `host_id`, `host_name`, `neighbourhood_group`, `neighbourhood`
- `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`
- `number_of_reviews`, `last_review`, `reviews_per_month`
- `calculated_host_listings_count`, `availability_365`

### Q: Where are exported CSV files saved?

**A:** Default location:
- Windows: `C:\Users\YourName\Documents\`
- macOS: `~/Documents/`
- Linux: `~/Documents/`

You can choose a different location in the save dialog.

### Q: Can I run this on a Raspberry Pi?

**A:** Yes, but performance may be limited. Recommended:
- Raspberry Pi 4 with 4GB+ RAM
- Use lightweight desktop environment (LXDE)
- Reduce data sample size if needed

### Q: How do I update to the latest version?

**A:** 
```bash
cd Data-Visualization-Project---NYC-Airbnb-Dashboard
git pull origin main
pip install --upgrade -r qt_app/requirements.txt
```

### Q: Why is the virtual environment recommended?

**A:** Virtual environments:
- Prevent package conflicts with other projects
- Make the project portable
- Allow different Python versions per project
- Keep your system Python clean

### Q: Can I customize the color theme?

**A:** Yes! Edit `qt_app/core/theme_manager.py`:
```python
THEMES = {
    'dark': {
        'bg_primary': '#0d1117',  # Change colors here
        'accent': '#58a6ff',
        # ... more colors
    }
}
```


## 📁 Project Structure

```
Data-Visualization-Project---NYC-Airbnb-Dashboard/
├── AB_NYC_2019.csv         # Dataset (48,895 Airbnb listings)
├── venv_qt/                # Virtual environment (created during setup)
└── qt_app/                 # Main application directory
    ├── main.py             # Application entry point
    ├── requirements.txt    # Python dependencies
    ├── README.md          # This file
    ├── core/              # Core application modules
    │   ├── main_window.py    # Main application window
    │   ├── theme_manager.py  # Dark/Light theme handling
    │   ├── data_manager.py   # Data loading and filtering
    │   └── animations.py     # Animation utilities
    ├── widgets/           # Reusable UI components
    │   ├── custom_widgets.py # Modern UI components (cards, badges)
    │   ├── sidebar.py        # Navigation sidebar
    │   ├── filter_panel.py   # Data filters interface
    │   └── charts.py         # Plotly chart widgets
    └── views/             # Stakeholder perspective views
        ├── base_view.py      # Base view class
        ├── traveler_view.py  # Traveler perspective (budget search)
        ├── investor_view.py  # Investor perspective (ROI analysis)
        ├── regulator_view.py # Regulator perspective (compliance)
        ├── competitor_view.py # Competitor perspective (hotel analysis)
        └── journalist_view.py # Journalist perspective (data stories)
```

## 🎨 Customization

### Changing Default Filters

Edit `qt_app/widgets/filter_panel.py`:

```python
def __init__(self, data_manager, parent=None):
    # Example: Start with only Manhattan and Brooklyn
    for borough in self.data_manager.get_all_boroughs():
        cb = QCheckBox(borough)
        cb.setChecked(borough in ['Manhattan', 'Brooklyn'])  # Custom default
    
    # Example: Start with $100-$200 price range
    self.price_slider = DoubleHandleSlider(100, 200, 0, 10000)
```

### Adding Custom Views

1. Create new file in `qt_app/views/your_view.py`
2. Extend `BaseView` class:

```python
from qt_app.views.base_view import BaseView

class YourView(BaseView):
    def _setup_content(self):
        # Set header info
        self.persona_badge.setText("👤 Your Persona")
        self.title_label.setText("Your Dashboard Title")
        
        # Add stat cards
        self.stat1 = self.add_stat_card("📊", "0", "Metric 1", "#58a6ff")
        
        # Add charts
        self.chart1 = self.add_chart(0, 0, 1, 2)
    
    def refresh(self):
        # Update visualizations with current data
        df = self.data_manager.filtered_df
        # ... your visualization code
```

3. Register in `qt_app/core/main_window.py`:

```python
def _setup_views(self):
    self._view_classes = {
        'your_view': 'qt_app.views.your_view.YourView',
    }
```

### Theme Customization

Edit `qt_app/core/theme_manager.py`:

```python
THEMES = {
    'dark': {
        'bg_primary': '#0d1117',      # Main background
        'bg_secondary': '#161b22',    # Card background
        'bg_tertiary': '#21262d',     # Input background
        'text_primary': '#e6edf3',    # Main text
        'text_secondary': '#8b949e',  # Secondary text
        'accent': '#58a6ff',          # Primary accent (blue)
        'accent_hover': '#79c0ff',    # Hover state
        'success': '#3fb950',         # Success color (green)
        'warning': '#d29922',         # Warning color (yellow)
        'danger': '#f85149',          # Danger color (red)
        'border': '#30363d',          # Border color
    },
    # Add custom theme
    'ocean': {
        'bg_primary': '#0a1929',
        'accent': '#00b4d8',
        # ... more colors
    }
}
```

## 🧪 Development

### Running in Development Mode

```bash
# Activate virtual environment
venv_qt\Scripts\activate  # Windows
source venv_qt/bin/activate  # macOS/Linux

# Run with Python debugger
python -m pdb -m qt_app.main

# Or with verbose logging
python -m qt_app.main --debug
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-qt

# Run all tests
pytest qt_app/tests/

# Run specific test file
pytest qt_app/tests/test_data_manager.py

# Run with coverage
pytest --cov=qt_app qt_app/tests/
```

### Code Style

This project follows:
- **PEP 8** for Python code style
- **Type hints** for function signatures
- **Docstrings** for all public methods

```bash
# Format code
pip install black
black qt_app/

# Check style
pip install flake8
flake8 qt_app/

# Type checking
pip install mypy
mypy qt_app/
```

## 📊 Dataset Information

### Source
- **Provider**: Inside Airbnb
- **Location**: New York City, USA
- **Year**: 2019
- **Format**: CSV (Comma-Separated Values)
- **Size**: ~10 MB, 48,895 rows, 16 columns

### Columns Description

| Column | Description | Type |
|--------|-------------|------|
| `id` | Unique listing identifier | Integer |
| `name` | Listing title/description | String |
| `host_id` | Unique host identifier | Integer |
| `host_name` | Host's name | String |
| `neighbourhood_group` | Borough (Manhattan, Brooklyn, etc.) | String |
| `neighbourhood` | Specific neighborhood name | String |
| `latitude` | Listing latitude coordinate | Float |
| `longitude` | Listing longitude coordinate | Float |
| `room_type` | Type (Entire home/Private/Shared) | String |
| `price` | Price per night (USD) | Integer |
| `minimum_nights` | Minimum stay requirement | Integer |
| `number_of_reviews` | Total number of reviews | Integer |
| `last_review` | Date of most recent review | Date |
| `reviews_per_month` | Average reviews per month | Float |
| `calculated_host_listings_count` | Number of listings per host | Integer |
| `availability_365` | Days available per year | Integer |

### Data Cleaning Applied

- Removed listings with price = $0
- Handled missing coordinates
- Standardized borough names
- Calculated derived fields:
  - `host_size`: Single/Small/Medium/Mega
  - `is_commercial`: Boolean flag for commercial operations
  - `estimated_revenue`: Annual revenue estimate
  - `value_score`: Reviews per dollar metric

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Data-Visualization-Project---NYC-Airbnb-Dashboard.git
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update README if needed

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and click "New Pull Request"
   - Describe your changes
   - Wait for review

### Contribution Guidelines

- Follow existing code style (PEP 8)
- Add docstrings to new functions/classes
- Test your changes thoroughly
- Keep commits focused and atomic
- Write clear commit messages

## 📄 License

MIT License

Copyright (c) 2026 Huseyin Soykok

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

- **Inside Airbnb** for providing open access to Airbnb data
- **Qt/PySide6** community for excellent documentation and support
- **Plotly** team for powerful interactive visualization library
- **GitHub** for hosting and version control
- All contributors who have helped improve this project

## 📞 Support

### Get Help

- **Issues**: [GitHub Issues](https://github.com/HuseyinSoykok/Data-Visualization-Project---NYC-Airbnb-Dashboard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HuseyinSoykok/Data-Visualization-Project---NYC-Airbnb-Dashboard/discussions)
- **Email**: Create an issue instead for faster response

### Reporting Bugs

When reporting bugs, please include:
1. Operating system and version
2. Python version (`python --version`)
3. Steps to reproduce
4. Expected vs actual behavior
5. Error messages or screenshots

### Feature Requests

To request features:
1. Check existing issues first
2. Create new issue with "Feature Request" label
3. Describe the feature and use case
4. Explain why it would be useful

## 🔄 Changelog

### Version 2.0.0 (2026-01-22)
- ✨ Complete rewrite using PySide6
- 🎨 Modern dark/light theme system
- 🚀 Performance improvements (3-6x faster)
- 📊 Enhanced visualizations with professional styling
- 🎯 Meaningful colorbar labels
- 📈 Statistical annotations (mean, median, quartiles)
- 🎨 Consistent color schemes across all views
- 💾 CSV export functionality
- ⌨️ Keyboard shortcuts
- 🐛 Bug fixes and stability improvements

### Version 1.0.0 (Previous)
- Initial Dash-based implementation
- Basic visualizations
- Limited filtering options

## 🗺️ Roadmap

### Planned Features

- [ ] Multi-language support (Turkish, Spanish, French)
- [ ] Real-time data updates via API
- [ ] Custom report generation (PDF export)
- [ ] Advanced statistical analysis tools
- [ ] Machine learning price predictions
- [ ] Mobile-responsive web version
- [ ] Database support (PostgreSQL, SQLite)
- [ ] User preferences and saved filters
- [ ] Comparison mode (compare two boroughs side-by-side)
- [ ] Historical data timeline view

### Future Enhancements

- [ ] Interactive tutorial for first-time users
- [ ] More customization options
- [ ] Plugin system for third-party extensions
- [ ] Cloud deployment guide
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

---

**Made with ❤️ by Huseyin Soykok**

*Last Updated: January 22, 2026*
