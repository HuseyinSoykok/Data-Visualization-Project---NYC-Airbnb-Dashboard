"""
Plotly Chart Widget - Embeds Plotly charts in Qt using WebEngine
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QUrl, Signal
import plotly.graph_objects as go
import plotly.express as px
import json


class PlotlyWidget(QWidget):
    """Widget for displaying Plotly charts"""
    
    chart_clicked = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_fig = None
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        
        # Enable settings for better performance and rendering
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)  # GPU acceleration
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)  # Enable WebGL for better chart performance
        
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.web_view)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def set_figure(self, fig: go.Figure, dark_mode: bool = True, show_colorbar: bool = True):
        """Set the Plotly figure to display
        
        Args:
            fig: Plotly figure to display
            dark_mode: Whether to use dark theme
            show_colorbar: Whether to show colorbar (default True, set False for bar/scatter charts)
        """
        self._current_fig = fig
        self._dark_mode = dark_mode
        self._show_colorbar = show_colorbar
        
        # Theme colors
        if dark_mode:
            bg_color = '#0d1117'
            paper_color = '#0d1117'
            text_color = '#e6edf3'
            grid_color = '#30363d'
            axis_color = '#8b949e'
            legend_bg = 'rgba(22, 27, 34, 0.9)'
            legend_border = '#30363d'
            title_color = '#e6edf3'
            tick_color = '#8b949e'
            colorbar_text = '#e6edf3'
        else:
            bg_color = '#ffffff'
            paper_color = '#ffffff'
            text_color = '#1f2328'
            grid_color = '#d0d7de'
            axis_color = '#656d76'
            legend_bg = 'rgba(255, 255, 255, 0.95)'
            legend_border = '#d0d7de'
            title_color = '#1f2328'
            tick_color = '#656d76'
            colorbar_text = '#1f2328'
        
        # Comprehensive layout update with performance optimizations
        fig.update_layout(
            template='plotly_dark' if dark_mode else 'plotly_white',
            paper_bgcolor=paper_color,
            plot_bgcolor=bg_color,
            font=dict(
                color=text_color, 
                family="Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif",
                size=12
            ),
            title=dict(
                font=dict(color=title_color, size=16, family="Segoe UI, sans-serif")
            ),
            margin=dict(l=50, r=30, t=60, b=50),
            legend=dict(
                bgcolor=legend_bg,
                bordercolor=legend_border,
                borderwidth=1,
                font=dict(color=text_color, size=11)
            ),
            xaxis=dict(
                gridcolor=grid_color, 
                zerolinecolor=grid_color,
                linecolor=grid_color,
                tickcolor=tick_color,
                tickfont=dict(color=tick_color, size=11),
                title_font=dict(color=axis_color, size=12),
                automargin=True  # Better performance
            ),
            yaxis=dict(
                gridcolor=grid_color, 
                zerolinecolor=grid_color,
                linecolor=grid_color,
                tickcolor=tick_color,
                tickfont=dict(color=tick_color, size=11),
                title_font=dict(color=axis_color, size=12),
                automargin=True  # Better performance
            ),
            # Performance optimizations
            hovermode='closest',  # Faster hover calculations
            dragmode='pan'  # Default to pan for better UX
        )
        
        # Handle colorbar visibility based on show_colorbar parameter
        if not show_colorbar:
            # Completely remove coloraxis
            fig.update_layout(coloraxis_showscale=False)
            if hasattr(fig.layout, 'coloraxis'):
                fig.layout.coloraxis = None
        elif hasattr(fig.layout, 'coloraxis') and fig.layout.coloraxis is not None:
            # Style the colorbar for theme
            fig.update_layout(
                coloraxis=dict(
                    colorbar=dict(
                        tickfont=dict(color=colorbar_text),
                        title_font=dict(color=colorbar_text),
                        outlinecolor=grid_color,
                        bgcolor=paper_color
                    )
                )
            )
        
        # Update all trace-level text and colorbar settings
        for trace in fig.data:
            # Update colorbar text or hide it
            if hasattr(trace, 'marker') and trace.marker is not None:
                if hasattr(trace.marker, 'colorbar') and trace.marker.colorbar is not None:
                    if not show_colorbar:
                        trace.marker.showscale = False
                    else:
                        trace.marker.colorbar.tickfont = dict(color=colorbar_text)
                        if trace.marker.colorbar.title is not None:
                            trace.marker.colorbar.title.font = dict(color=colorbar_text)
            
            # Update pie chart text
            if trace.type == 'pie':
                trace.textfont = dict(color=text_color)
                trace.insidetextfont = dict(color='#ffffff')  # White for better contrast on pie slices
                trace.outsidetextfont = dict(color=text_color)
            
            # Update bar chart text
            if trace.type == 'bar':
                if hasattr(trace, 'textfont'):
                    trace.textfont = dict(color=text_color)
            
            # Update scatter text
            if trace.type in ['scatter', 'scattergl']:
                if hasattr(trace, 'textfont'):
                    trace.textfont = dict(color=text_color)
        
        # Generate HTML
        html = self._generate_html(fig, dark_mode)
        self.web_view.setHtml(html)
    
    def _generate_html(self, fig: go.Figure, dark_mode: bool = True) -> str:
        """Generate HTML content for the chart with proper theme styling"""
        chart_json = fig.to_json()
        
        # Theme-specific colors for HTML/CSS
        if dark_mode:
            body_bg = '#0d1117'
            modebar_bg = 'rgba(22, 27, 34, 0.95)'
            modebar_color = '#8b949e'
            modebar_hover = '#e6edf3'
            modebar_active = '#58a6ff'
            tooltip_bg = '#21262d'
            tooltip_text = '#e6edf3'
            tooltip_border = '#30363d'
        else:
            body_bg = '#ffffff'
            modebar_bg = 'rgba(255, 255, 255, 0.95)'
            modebar_color = '#656d76'
            modebar_hover = '#1f2328'
            modebar_active = '#0969da'
            tooltip_bg = '#ffffff'
            tooltip_text = '#1f2328'
            tooltip_border = '#d0d7de'
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    background-color: {body_bg};
                    overflow: hidden;
                    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
                }}
                #chart {{
                    width: 100%;
                    height: 100vh;
                }}
                
                /* Modebar styling */
                .modebar {{
                    background-color: {modebar_bg} !important;
                    border-radius: 6px !important;
                    padding: 4px !important;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
                }}
                .modebar-btn {{
                    color: {modebar_color} !important;
                }}
                .modebar-btn:hover {{
                    color: {modebar_hover} !important;
                }}
                .modebar-btn.active {{
                    color: {modebar_active} !important;
                }}
                .modebar-btn svg {{
                    fill: currentColor !important;
                }}
                
                /* Tooltip/Hover styling */
                .hoverlayer .hovertext {{
                    background-color: {tooltip_bg} !important;
                }}
                .hoverlayer .hovertext text {{
                    fill: {tooltip_text} !important;
                }}
                .hoverlayer .hovertext path {{
                    stroke: {tooltip_border} !important;
                    fill: {tooltip_bg} !important;
                }}
                
                /* Legend styling */
                .legend {{
                    background-color: {modebar_bg} !important;
                }}
                .legend text {{
                    fill: {tooltip_text} !important;
                }}
                
                /* Colorbar text and labels */
                .colorbar text {{
                    fill: {tooltip_text} !important;
                }}
                .cbtitle text {{
                    fill: {tooltip_text} !important;
                }}
                .cbticks text {{
                    fill: {tooltip_text} !important;
                }}
                
                /* Axis labels and titles */
                .xtick text, .ytick text {{
                    fill: {tooltip_text} !important;
                }}
                .xtitle, .ytitle {{
                    fill: {tooltip_text} !important;
                }}
                .gtitle {{
                    fill: {tooltip_text} !important;
                }}
                
                /* Pie chart labels */
                .pieslices text {{
                    fill: {tooltip_text} !important;
                }}
                .pielayer .slicetext {{
                    fill: {tooltip_text} !important;
                }}
                
                /* Bar chart text */
                .trace.bars text {{
                    fill: {tooltip_text} !important;
                }}
                
                /* Annotation text */
                .annotation text {{
                    fill: {tooltip_text} !important;
                }}
            </style>
        </head>
        <body>
            <div id="chart"></div>
            <script>
                var figure = {chart_json};
                var config = {{
                    responsive: true,
                    displayModeBar: true,
                    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
                    displaylogo: false,
                    scrollZoom: true,
                    doubleClick: 'reset',  // Faster double-click reset
                    toImageButtonOptions: {{
                        format: 'png',
                        filename: 'chart',
                        height: 800,
                        width: 1200,
                        scale: 2
                    }}
                }};
                
                Plotly.newPlot('chart', figure.data, figure.layout, config);
                
                // Handle resize
                window.addEventListener('resize', function() {{
                    Plotly.Plots.resize('chart');
                }});
                
                // Handle click events
                document.getElementById('chart').on('plotly_click', function(data) {{
                    var info = {{
                        x: data.points[0].x,
                        y: data.points[0].y,
                        text: data.points[0].text || '',
                        customdata: data.points[0].customdata || null
                    }};
                    console.log(JSON.stringify(info));
                }});
            </script>
        </body>
        </html>
        '''
        return html
    
    def clear(self):
        """Clear the chart"""
        self.web_view.setHtml("")
        self._current_fig = None
    
    def export_image(self, filename: str, format: str = 'png'):
        """Export chart as image"""
        if self._current_fig:
            self._current_fig.write_image(filename, format=format, scale=2)


class MapWidget(PlotlyWidget):
    """Specialized widget for Plotly maps"""
    
    def __init__(self, mapbox_token: str = None, parent=None):
        super().__init__(parent)
        self.mapbox_token = mapbox_token
    
    def set_map_figure(self, fig: go.Figure, dark_mode: bool = True):
        """Set map figure with appropriate styling"""
        map_style = 'carto-darkmatter' if dark_mode else 'carto-positron'
        
        # Theme colors for map
        if dark_mode:
            text_color = '#e6edf3'
            legend_bg = 'rgba(22, 27, 34, 0.95)'
            legend_border = '#30363d'
            colorbar_text = '#e6edf3'
        else:
            text_color = '#1f2328'
            legend_bg = 'rgba(255, 255, 255, 0.95)'
            legend_border = '#d0d7de'
            colorbar_text = '#1f2328'
        
        fig.update_layout(
            mapbox=dict(
                style=map_style,
                center=dict(lat=40.7128, lon=-74.0060),
                zoom=10,
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(color=text_color),
            legend=dict(
                bgcolor=legend_bg,
                bordercolor=legend_border,
                borderwidth=1,
                font=dict(color=text_color)
            ),
            coloraxis=dict(
                colorbar=dict(
                    tickfont=dict(color=colorbar_text),
                    title_font=dict(color=colorbar_text)
                )
            )
        )
        
        # Update colorbar for scatter mapbox traces
        for trace in fig.data:
            if hasattr(trace, 'marker') and trace.marker is not None:
                if hasattr(trace.marker, 'colorbar') and trace.marker.colorbar is not None:
                    trace.marker.colorbar.tickfont = dict(color=colorbar_text)
                    if trace.marker.colorbar.title is not None:
                        trace.marker.colorbar.title.font = dict(color=colorbar_text)
        
        self.set_figure(fig, dark_mode)


class ChartFactory:
    """Factory for creating common chart types"""
    
    @staticmethod
    def create_bar_chart(x, y, title: str = "", color: str = "#58a6ff") -> go.Figure:
        fig = go.Figure(data=[
            go.Bar(x=x, y=y, marker_color=color)
        ])
        fig.update_layout(title=title)
        return fig
    
    @staticmethod
    def create_line_chart(x, y, title: str = "", color: str = "#58a6ff") -> go.Figure:
        fig = go.Figure(data=[
            go.Scatter(x=x, y=y, mode='lines+markers', line=dict(color=color, width=2))
        ])
        fig.update_layout(title=title)
        return fig
    
    @staticmethod
    def create_pie_chart(labels, values, title: str = "") -> go.Figure:
        colors = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#a371f7']
        fig = go.Figure(data=[
            go.Pie(labels=labels, values=values, marker=dict(colors=colors))
        ])
        fig.update_layout(title=title)
        return fig
    
    @staticmethod
    def create_scatter_map(df, lat_col: str, lon_col: str, color_col: str = None,
                          size_col: str = None, hover_data: list = None,
                          title: str = "") -> go.Figure:
        fig = px.scatter_mapbox(
            df,
            lat=lat_col,
            lon=lon_col,
            color=color_col,
            size=size_col,
            hover_data=hover_data,
            title=title,
            zoom=10,
        )
        return fig
    
    @staticmethod
    def create_histogram(data, nbins: int = 50, title: str = "", 
                        color: str = "#58a6ff") -> go.Figure:
        fig = go.Figure(data=[
            go.Histogram(x=data, nbinsx=nbins, marker_color=color)
        ])
        fig.update_layout(title=title)
        return fig
    
    @staticmethod
    def create_box_plot(df, x_col: str, y_col: str, title: str = "") -> go.Figure:
        fig = px.box(df, x=x_col, y=y_col, title=title)
        return fig
    
    @staticmethod
    def create_violin_plot(df, x_col: str, y_col: str, title: str = "") -> go.Figure:
        fig = px.violin(df, x=x_col, y=y_col, box=True, title=title)
        return fig
    
    @staticmethod
    def create_heatmap(z, x_labels, y_labels, title: str = "") -> go.Figure:
        fig = go.Figure(data=[
            go.Heatmap(z=z, x=x_labels, y=y_labels, colorscale='Blues')
        ])
        fig.update_layout(title=title)
        return fig
