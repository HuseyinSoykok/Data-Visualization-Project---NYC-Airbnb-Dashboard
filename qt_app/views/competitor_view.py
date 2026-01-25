"""
Competitor View - For hotel industry professionals
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider
from PySide6.QtCore import Qt

from qt_app.views.base_view import BaseView
from qt_app.widgets.custom_widgets import ModernCard


class CompetitorView(BaseView):
    """View for Competitor persona (Maria) - Hotel Industry"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.heatmap_radius = 15  # Default density heatmap radius
    
    def _setup_content(self):
        # Set header info
        self.persona_badge.setText("🏨 Hotel Competitor Persona")
        self.title_label.setText("Competitive Analysis Dashboard")
        self.desc_label.setText(
            "As Maria, a hotel industry analyst, understand the Airbnb competitive landscape, "
            "pricing strategies, and market positioning to inform your hotel strategy."
        )
        
        # Stat cards - always colorful (not affected by grayscale mode)
        self.market_size_card = self.add_stat_card("📊", "0", "Total Airbnb Supply", "#58a6ff")
        self.entire_home_card = self.add_stat_card("🏠", "0%", "Hotel-Like (Entire Home)", "#f85149")
        self.avg_price_card = self.add_stat_card("💰", "$0", "Avg Airbnb Price", "#3fb950")
        self.price_advantage_card = self.add_stat_card("📈", "0%", "Under $150/night", "#d29922")
        
        # Charts
        self.density_map = self.add_chart(0, 0, 1, 2)
        
        # Add heatmap intensity slider control right after the map
        slider_container = QWidget()
        slider_layout = QHBoxLayout(slider_container)
        slider_layout.setContentsMargins(0, 8, 0, 16)
        
        slider_label = QLabel("🔥 Heatmap Intensity:")
        slider_label.setStyleSheet("font-weight: 600; font-size: 13px;")
        slider_layout.addWidget(slider_label)
        
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(5, 50)  # Radius from 5 to 50
        self.intensity_slider.setValue(15)  # Default
        self.intensity_slider.setTickInterval(5)
        self.intensity_slider.setFixedWidth(200)
        self.intensity_slider.setToolTip("Adjust the competition heatmap density (lower = sharper hotspots, higher = broader patterns)")
        self.intensity_slider.valueChanged.connect(self._on_intensity_changed)
        slider_layout.addWidget(self.intensity_slider)
        
        self.intensity_value_label = QLabel("15")
        self.intensity_value_label.setStyleSheet("font-size: 13px; min-width: 30px;")
        slider_layout.addWidget(self.intensity_value_label)
        
        slider_layout.addStretch()
        self.content_layout.addWidget(slider_container)
        
        self.price_comparison = self.add_chart(1, 0)
        self.room_competition = self.add_chart(1, 1)
        self.location_analysis = self.add_chart(2, 0)
        self.market_share = self.add_chart(2, 1)
        
        # Competitive insights
        insights_card = self.create_info_card(
            "🎯 Competitive Insights",
            "• Airbnb captures budget-conscious travelers under $150/night\n"
            "• Entire homes compete directly with suite hotels\n"
            "• Manhattan has highest density of hotel alternatives\n"
            "• Private rooms serve a different market segment\n"
            "• Focus on amenities and services Airbnb can't match"
        )
        self.content_layout.addWidget(insights_card)
        
        # Strategy recommendations
        strategy_card = self.create_info_card(
            "💼 Strategic Recommendations",
            "• Differentiate through concierge and 24/7 services\n"
            "• Target business travelers needing consistent quality\n"
            "• Offer competitive extended stay rates\n"
            "• Highlight safety and security advantages\n"
            "• Partner with corporate clients for guaranteed bookings"
        )
        self.content_layout.addWidget(strategy_card)
    
    def refresh(self):
        """Refresh all visualizations with current data"""
        df = self.data_manager.filtered_df
        if df is None or len(df) == 0:
            return
        
        is_dark = self.theme_manager.current_theme == 'dark'
        
        # Update view theme
        self._update_view_theme(is_dark)
        
        # Update widget themes
        self._update_widget_themes(is_dark)
        
        # Update stats
        total_supply = len(df)
        self.market_size_card.set_value(f"{total_supply:,}")
        
        entire_homes = len(df[df['room_type'] == 'Entire home/apt'])
        entire_home_pct = entire_homes / total_supply * 100 if total_supply > 0 else 0
        self.entire_home_card.set_value(f"{entire_home_pct:.1f}%")
        
        avg_price = df['price'].mean()
        self.avg_price_card.set_value(f"${avg_price:.0f}")
        
        budget_listings = len(df[df['price'] < 150])
        budget_pct = budget_listings / total_supply * 100 if total_supply > 0 else 0
        self.price_advantage_card.set_value(f"{budget_pct:.1f}%")
        
        # Density Heatmap with enhanced colors
        colorbar_text = '#e6edf3' if is_dark else '#1f2328'
        
        # Grayscale-aware color scale
        if self.theme_manager.grayscale_mode:
            color_scale = [
                [0.0, '#f0f0f0'],   # Very light gray (low competition)
                [0.25, '#c0c0c0'],  # Light gray
                [0.5, '#808080'],   # Medium gray
                [0.75, '#404040'],  # Dark gray
                [1.0, '#1a1a1a']    # Very dark gray (high competition)
            ]
        else:
            color_scale = [
                [0.0, '#e0f3db'],   # Very light green (low competition)
                [0.25, '#a8ddb5'],  # Light green
                [0.5, '#43a2ca'],   # Blue
                [0.75, '#0868ac'],  # Dark blue
                [1.0, '#023858']    # Very dark blue (high competition)
            ]
        
        fig_density = px.density_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            radius=self.heatmap_radius,  # Use configurable radius
            title='🗺️ Airbnb Density Heatmap - Competition Hotspots',
            zoom=10,
            center=dict(lat=40.7128, lon=-74.0060),
            color_continuous_scale=color_scale
        )
        fig_density.update_layout(
            mapbox_style='carto-darkmatter' if is_dark else 'carto-positron',
            height=650,
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                title=dict(text="Competition Level", font=dict(color=colorbar_text, size=12)),
                tickfont=dict(color=colorbar_text, size=10),
                thickness=15,
                len=0.7,
                x=1.02,
                xanchor='left',
                bgcolor='rgba(0,0,0,0)',
                outlinewidth=0,
                tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High']
            )
        )
        self.density_map.set_figure(fig_density, is_dark)
        
        # Price Comparison Box Plot
        room_colors = self._get_room_type_colors()
        
        fig_price = px.box(
            df,
            x='neighbourhood_group',
            y='price',
            color='room_type',
            color_discrete_map=room_colors,
            title='💰 Price Distribution: Airbnb vs Hotel Price Points',
            labels={'neighbourhood_group': 'Borough', 'price': 'Price ($)'}
        )
        # Add hotel benchmark lines
        benchmark_color1 = '#808080' if self.theme_manager.grayscale_mode else '#f85149'
        benchmark_color2 = '#a0a0a0' if self.theme_manager.grayscale_mode else '#d29922'
        
        fig_price.add_hline(y=150, line_dash="dash", line_color=benchmark_color1,
                          annotation_text="Budget Hotel (~$150)", annotation_position="top right")
        fig_price.add_hline(y=250, line_dash="dash", line_color=benchmark_color2,
                          annotation_text="Mid-Range Hotel (~$250)", annotation_position="top right")
        fig_price.update_layout(
            height=400,
            xaxis_title='Borough',
            yaxis_title='Price per Night (USD)',
            yaxis=dict(tickformat='$,.0f')
        )
        fig_price.update_yaxes(range=[0, 500])
        self.price_comparison.set_figure(fig_price, is_dark)
        
        # Room Type Competition Analysis
        room_stats = df.groupby('room_type').agg({
            'id': 'count',
            'price': 'mean',
            'number_of_reviews': 'sum'
        }).reset_index()
        room_stats.columns = ['Room Type', 'Count', 'Avg Price', 'Total Reviews']
        
        # Grayscale-aware colors
        bar_color = '#808080' if self.theme_manager.grayscale_mode else '#58a6ff'
        line_color = '#606060' if self.theme_manager.grayscale_mode else '#f85149'
        
        fig_room = go.Figure(data=[
            go.Bar(name='Listings', x=room_stats['Room Type'], 
                   y=room_stats['Count'], yaxis='y', marker_color=bar_color),
            go.Scatter(name='Avg Price', x=room_stats['Room Type'], 
                      y=room_stats['Avg Price'], yaxis='y2', 
                      mode='lines+markers', line=dict(color=line_color, width=3))
        ])
        fig_room.update_layout(
            title='🏠 Room Type Market Analysis',
            xaxis_title='Room Type',
            yaxis=dict(title='Number of Listings', side='left', tickformat=',d'),
            yaxis2=dict(title='Average Price (USD)', side='right', overlaying='y', tickformat='$,.0f'),
            height=350,
            legend=dict(x=0.7, y=1.1, orientation='h')
        )
        self.room_competition.set_figure(fig_room, is_dark, show_colorbar=False)
        
        # Location Analysis - Hotel Districts vs Airbnb
        location_data = df.groupby(['neighbourhood_group', 'room_type']).size().reset_index()
        location_data.columns = ['Borough', 'Room Type', 'Count']
        
        # Grayscale-aware room type colors
        room_type_colors = self._get_room_type_colors()
        
        fig_location = px.bar(
            location_data,
            x='Borough',
            y='Count',
            color='Room Type',
            color_discrete_map=room_type_colors,
            title='📍 Airbnb Supply by Borough & Type',
            barmode='stack'
        )
        fig_location.update_layout(
            height=350,
            xaxis_title='Borough',
            yaxis_title='Number of Listings',
            yaxis=dict(tickformat=',d')
        )
        self.location_analysis.set_figure(fig_location, is_dark, show_colorbar=False)
        
        # Market Share by Price Tier
        df_tiers = df.copy()
        df_tiers['price_tier'] = pd.cut(
            df_tiers['price'],
            bins=[0, 75, 150, 250, 500, 1000],
            labels=['Budget (<$75)', 'Economy ($75-150)', 'Mid-Range ($150-250)', 
                   'Upscale ($250-500)', 'Luxury ($500+)']
        )
        
        tier_data = df_tiers.groupby('price_tier').size().reset_index()
        tier_data.columns = ['Price Tier', 'Count']
        
        pie_colors = ['#e0e0e0', '#c0c0c0', '#a0a0a0', '#808080', '#606060'] if self.theme_manager.grayscale_mode else ['#3fb950', '#58a6ff', '#d29922', '#f85149', '#a371f7']
        
        fig_share = px.pie(
            tier_data,
            values='Count',
            names='Price Tier',
            title='💎 Market Share by Price Tier',
            color_discrete_sequence=pie_colors
        )
        fig_share.update_layout(height=350)
        fig_share.update_traces(textposition='inside', textinfo='percent+label')
        self.market_share.set_figure(fig_share, is_dark)
    
    def _get_room_type_colors(self):
        """Get room type colors based on grayscale mode"""
        if self.theme_manager.grayscale_mode:
            return {
                'Entire home/apt': '#1a1a1a',
                'Private room': '#666666',
                'Shared room': '#b3b3b3'
            }
        else:
            return {
                'Entire home/apt': '#3b82f6',
                'Private room': '#10b981',
                'Shared room': '#f59e0b'
            }
    
    def _on_intensity_changed(self, value: int):
        """Handle heatmap intensity slider change"""
        self.heatmap_radius = value
        self.intensity_value_label.setText(str(value))
        self.refresh()
    
    def _update_widget_themes(self, is_dark: bool):
        """Update custom widget themes"""
        if is_dark:
            slider_style = """
                QSlider::groove:horizontal {
                    background: #21262d;
                    height: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #58a6ff;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }
                QSlider::handle:horizontal:hover {
                    background: #79c0ff;
                }
            """
            text_color = "#e6edf3"
        else:
            slider_style = """
                QSlider::groove:horizontal {
                    background: #eaeef2;
                    height: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #0969da;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }
                QSlider::handle:horizontal:hover {
                    background: #0860ca;
                }
            """
            text_color = "#1f2328"
        
        self.intensity_slider.setStyleSheet(slider_style)
        self.intensity_value_label.setStyleSheet(f"color: {text_color}; font-size: 13px; min-width: 30px;")
