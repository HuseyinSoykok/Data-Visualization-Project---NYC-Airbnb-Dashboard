"""
Traveler View - For tourists/travelers seeking accommodation
Enhanced with app_en.py features: value score table, better map legend
"""

import plotly.express as px
import plotly.graph_objects as go
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt

from qt_app.views.base_view import BaseView
from qt_app.widgets.custom_widgets import ModernCard, Badge


class TravelerView(BaseView):
    """View for Traveler persona (Hüseyin)"""
    
    def _setup_content(self):
        # Set header info
        self.persona_badge.setText("🧳 Traveler Persona")
        self.title_label.setText("Find Your Perfect Stay")
        self.desc_label.setText(
            "As Hüseyin, a budget-conscious traveler, explore NYC accommodations to find "
            "the best value for your money. Compare prices across boroughs and room types."
        )
        
        # Add data quality indicators
        self.add_data_quality_indicators()
        
        # Stat cards - colors adapt to grayscale mode
        card_colors = self._get_stat_card_colors()
        self.total_card = self.add_stat_card("🏠", "0", "Available Listings", card_colors[0])
        self.avg_price_card = self.add_stat_card("💰", "$0", "Average Price/Night", card_colors[1])
        self.budget_card = self.add_stat_card("🎯", "0", "Budget Options (<$200)", card_colors[2])
        self.best_value_card = self.add_stat_card("⭐", "-", "Best Value Borough", card_colors[3])
        
        # Task info card
        task_card = self.create_info_card(
            "🎯 Hüseyin's Task",
            "Discover budget-friendly ($100-200), popular (100+ reviews) 'Entire home/apt' listings on the map.\n\n"
            "💡 Tip: Large green dots = Low price + High popularity = Best Value!"
        )
        self.content_layout.addWidget(task_card)
        
        # Charts
        self.price_map = self.add_chart(0, 0, 1, 2)
        self.price_dist_chart = self.add_chart(1, 0)
        self.borough_chart = self.add_chart(1, 1)
        self.room_type_chart = self.add_chart(2, 0)
        self.value_chart = self.add_chart(2, 1)
        
        # Map legend card
        self._setup_map_legend()
        
        # Top Value Listings Table
        self._setup_value_table()
        
        # Tips section
        tips_card = self.create_info_card(
            "💡 Traveler Tips",
            "• Look for private rooms in Brooklyn for best value\n"
            "• Book listings with high reviews for quality assurance\n"
            "• Consider longer stays for better nightly rates\n"
            "• Staten Island offers affordable options with fewer tourists"
        )
        self.content_layout.addWidget(tips_card)
    
    def _setup_map_legend(self):
        """Setup map legend card"""
        self.legend_card = ModernCard()
        legend_layout = QVBoxLayout(self.legend_card)
        legend_layout.setContentsMargins(16, 16, 16, 16)
        legend_layout.setSpacing(8)
        
        self.legend_title = QLabel("🎨 Map Legend")
        self.legend_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #e6edf3; background: transparent;")
        legend_layout.addWidget(self.legend_title)
        
        # Legend items
        legend_items = [
            ("●", "#2ecc71", "Budget-Friendly (< $200)"),
            ("●", "#f39c12", "Mid-Range ($200-$300)"),
            ("●", "#e74c3c", "Premium (> $300)"),
        ]
        
        self.legend_labels = []
        for symbol, color, text in legend_items:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(8)
            
            symbol_label = QLabel(symbol)
            symbol_label.setStyleSheet(f"color: {color}; font-size: 20px; background: transparent;")
            item_layout.addWidget(symbol_label)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #8b949e; font-size: 12px; background: transparent;")
            self.legend_labels.append(text_label)
            item_layout.addWidget(text_label)
            item_layout.addStretch()
            
            legend_layout.addWidget(item_widget)
        
        # Size legend
        size_widget = QWidget()
        size_layout = QHBoxLayout(size_widget)
        size_layout.setContentsMargins(0, 4, 0, 0)
        size_layout.setSpacing(4)
        
        small_dot = QLabel("⬤")
        small_dot.setStyleSheet("font-size: 8px; color: #8b949e; background: transparent;")
        size_layout.addWidget(small_dot)
        
        self.size_label = QLabel("Small = Few Reviews  |  ")
        self.size_label.setStyleSheet("color: #8b949e; font-size: 11px; background: transparent;")
        size_layout.addWidget(self.size_label)
        
        large_dot = QLabel("⬤")
        large_dot.setStyleSheet("font-size: 16px; color: #8b949e; background: transparent;")
        size_layout.addWidget(large_dot)
        
        self.size_label2 = QLabel("Large = Many Reviews")
        self.size_label2.setStyleSheet("color: #8b949e; font-size: 11px; background: transparent;")
        size_layout.addWidget(self.size_label2)
        size_layout.addStretch()
        
        legend_layout.addWidget(size_widget)
        
        self.content_layout.addWidget(self.legend_card)
    
    def _setup_value_table(self):
        """Setup top value listings table"""
        self.table_card = ModernCard()
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        
        # Table header
        header_layout = QHBoxLayout()
        self.table_title = QLabel("🏆 Top 10 Best Value Listings")
        self.table_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #e6edf3; background: transparent;")
        header_layout.addWidget(self.table_title)
        header_layout.addStretch()
        
        self.table_subtitle = QLabel("Ranked by Value Score (Reviews / Price)")
        self.table_subtitle.setStyleSheet("font-size: 12px; color: #8b949e; background: transparent;")
        header_layout.addWidget(self.table_subtitle)
        table_layout.addLayout(header_layout)
        
        # Table
        self.value_table = QTableWidget()
        self.value_table.setColumnCount(7)
        self.value_table.setHorizontalHeaderLabels([
            'Listing Name', 'Neighbourhood', 'Price', 'Reviews', 'Min Nights', 'Type', 'Value Score'
        ])
        self.value_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 7):
            self.value_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.value_table.setMinimumHeight(300)
        self._update_table_theme(True)
        table_layout.addWidget(self.value_table)
        
        self.content_layout.addWidget(self.table_card)
    
    def _update_table_theme(self, is_dark: bool):
        """Update table theme colors"""
        if is_dark:
            self.value_table.setStyleSheet("""
                QTableWidget {
                    background-color: #0d1117;
                    border: 1px solid #21262d;
                    border-radius: 8px;
                    gridline-color: #21262d;
                    color: #e6edf3;
                }
                QTableWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #21262d;
                    color: #e6edf3;
                }
                QHeaderView::section {
                    background-color: #161b22;
                    color: #e6edf3;
                    padding: 10px;
                    border: none;
                    font-weight: 600;
                }
            """)
        else:
            self.value_table.setStyleSheet("""
                QTableWidget {
                    background-color: #ffffff;
                    border: 1px solid #d0d7de;
                    border-radius: 8px;
                    gridline-color: #d0d7de;
                    color: #1f2328;
                }
                QTableWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #d0d7de;
                    color: #1f2328;
                }
                QHeaderView::section {
                    background-color: #f6f8fa;
                    color: #1f2328;
                    padding: 10px;
                    border: none;
                    font-weight: 600;
                }
            """)
    
    def refresh(self):
        """Refresh all visualizations with current data"""
        df = self.data_manager.filtered_df
        if df is None or len(df) == 0:
            return
        
        is_dark = self.theme_manager.current_theme == 'dark'
        
        # Update view theme
        self._update_view_theme(is_dark)
        
        # Update table theme
        self._update_table_theme(is_dark)
        title_color = "#e6edf3" if is_dark else "#1f2328"
        subtitle_color = "#8b949e" if is_dark else "#656d76"
        self.table_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {title_color}; background: transparent;")
        self.table_subtitle.setStyleSheet(f"font-size: 12px; color: {subtitle_color}; background: transparent;")
        self.legend_title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {title_color}; background: transparent;")
        for lbl in self.legend_labels:
            lbl.setStyleSheet(f"color: {subtitle_color}; font-size: 12px; background: transparent;")
        self.size_label.setStyleSheet(f"color: {subtitle_color}; font-size: 11px; background: transparent;")
        self.size_label2.setStyleSheet(f"color: {subtitle_color}; font-size: 11px; background: transparent;")
        
        # Update legend card background
        card_bg = "#161b22" if is_dark else "#ffffff"
        card_border = "#30363d" if is_dark else "#d0d7de"
        self.legend_card.setStyleSheet(f"""
            ModernCard {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 12px;
            }}
        """)
        self.table_card.setStyleSheet(f"""
            ModernCard {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 12px;
            }}
        """)
        
        # Update stats
        stats = self.data_manager.get_stats()
        self.total_card.set_value(f"{stats['total_listings']:,}")
        self.avg_price_card.set_value(f"${stats['avg_price']:.0f}")
        
        budget_count = len(df[df['price'] < 200])
        self.budget_card.set_value(f"{budget_count:,}")
        
        # Find best value borough (lowest avg price)
        borough_prices = df.groupby('neighbourhood_group')['price'].mean()
        best_value = borough_prices.idxmin() if len(borough_prices) > 0 else "-"
        self.best_value_card.set_value(str(best_value))
        
        # Price Map with better color scale (matching app_en.py)
        map_data = self.data_manager.get_map_data(3000)
        
        # Color scale: green (low) -> yellow (mid) -> red (high)
        if self.theme_manager.grayscale_mode:
            # Grayscale color scale
            PRICE_COLORSCALE = [[0, '#e0e0e0'], [0.5, '#808080'], [1, '#1a1a1a']]
        else:
            # Normal color scale
            PRICE_COLORSCALE = [[0, '#2ecc71'], [0.5, '#f39c12'], [1, '#e74c3c']]
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='latitude',
            lon='longitude',
            color='price',
            size='number_of_reviews',
            size_max=35,
            color_continuous_scale=PRICE_COLORSCALE,
            hover_name='name',
            hover_data={
                'price': ':$,.0f',
                'number_of_reviews': ':,.0f',
                'room_type': True,
                'neighbourhood': True,
                'neighbourhood_group': ':<b>Borough</b>',
                'availability_365': ':.0f days available',
                'minimum_nights': ':.0f night minimum',
                'latitude': False,
                'longitude': False
            },
            title='🗺️ Value-Focused Listing Map - Price and Popularity Analysis',
            zoom=10,
            center=dict(lat=40.7128, lon=-74.0060)
        )
        # Set minimum marker size for better visibility
        fig_map.update_traces(marker=dict(sizemin=8))
        fig_map.update_layout(
            mapbox_style='carto-darkmatter' if is_dark else 'carto-positron',
            height=800,
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title=dict(text="Price (USD)", font=dict(size=12)),
                tickformat="$,.0f",
                thickness=15,
                len=0.5,
                x=1.02,
                xanchor='left'
            ),
            dragmode='zoom',
            legend=dict(
                title=dict(text="Marker Size", font=dict(size=11)),
                orientation='v',
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=0.01,
                bgcolor='rgba(0,0,0,0.5)' if is_dark else 'rgba(255,255,255,0.8)',
                bordercolor='#30363d' if is_dark else '#d0d7de',
                borderwidth=1
            )
        )
        self.price_map.set_figure(fig_map, is_dark)
        self.price_map.set_accessible_info(
            "Price Map",
            "Interactive map showing NYC Airbnb listings colored by price. Green indicates budget-friendly options, red indicates expensive listings. Marker size represents popularity based on number of reviews."
        )
        
        # Price Distribution
        price_data = df[df['price'] <= 500]['price']
        
        if len(price_data) > 0:
            mean_price = price_data.mean()
            median_price = price_data.median()
            
            # Grayscale-aware colors
            hist_color = '#808080' if self.theme_manager.grayscale_mode else '#58a6ff'
            mean_color = '#606060' if self.theme_manager.grayscale_mode else '#f85149'
            median_color = '#a0a0a0' if self.theme_manager.grayscale_mode else '#3fb950'
            
            fig_price = go.Figure()
            fig_price.add_trace(go.Histogram(
                x=price_data,
                nbinsx=50,
                marker_color=hist_color,
                opacity=0.85,
                name='Listings'
            ))
            # Add mean line
            fig_price.add_vline(
                x=mean_price,
                line_dash="dash",
                line_color=mean_color,
                annotation_text=f"Mean: ${mean_price:.0f}",
                annotation_position="top right"
            )
            # Add median line
            fig_price.add_vline(
                x=median_price,
                line_dash="dot",
                line_color=median_color,
                annotation_text=f"Median: ${median_price:.0f}",
                annotation_position="top left"
            )
            fig_price.update_layout(
                title='💰 Price Distribution (Listings ≤ $500)',
                xaxis_title='Price per Night (USD)',
                yaxis_title='Number of Listings',
                height=380,
                bargap=0.05,
                showlegend=False,
                xaxis=dict(tickformat='$,.0f'),
                yaxis=dict(tickformat=',d')
            )
            self.price_dist_chart.set_figure(fig_price, is_dark, show_colorbar=False)
        else:
            # Empty state with actionable guidance
            fig_price = go.Figure()
            fig_price.add_annotation(
                text="<b>No price data available</b><br><br>"
                     "🔍 Try these steps:<br>"
                     "• Remove price filters to see more listings<br>"
                     "• Select different boroughs or room types<br>"
                     "• Reset all filters to view full dataset",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=13, color="#8b949e"),
                align="center"
            )
            fig_price.update_layout(
                title='💰 Price Distribution',
                height=350,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            self.price_dist_chart.set_figure(fig_price, is_dark, show_colorbar=False)
        
        # Borough Comparison
        borough_stats = df.groupby('neighbourhood_group').agg({
            'price': 'mean',
            'id': 'count'
        }).reset_index()
        borough_stats.columns = ['Borough', 'Avg Price', 'Listings']
        
        if len(borough_stats) > 0:
            # Consistent borough color mapping
            if self.theme_manager.grayscale_mode:
                # Grayscale mode: use different shades of gray
                borough_color_map = {
                    'Manhattan': '#1a1a1a',
                    'Brooklyn': '#404040',
                    'Queens': '#666666',
                    'Bronx': '#8c8c8c',
                    'Staten Island': '#b3b3b3'
                }
            else:
                # Normal color mode
                borough_color_map = {
                    'Manhattan': '#f59e0b',
                    'Brooklyn': '#ef4444',
                    'Queens': '#10b981',
                    'Bronx': '#3b82f6',
                    'Staten Island': '#8b5cf6'
                }
            
            fig_borough = px.bar(
                borough_stats,
                x='Borough',
                y='Avg Price',
                color='Borough',
                color_discrete_map=borough_color_map,
                title='🏙️ Average Price by Borough',
                text='Avg Price'
            )
            fig_borough.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            fig_borough.update_layout(
                height=380,
                showlegend=False,
                xaxis_title='Borough',
                yaxis_title='Average Price per Night (USD)',
                yaxis=dict(tickformat='$,.0f')
            )
            self.borough_chart.set_figure(fig_borough, is_dark, show_colorbar=False)
            self.borough_chart.set_accessible_info(
                "Borough Price Comparison",
                "Bar chart comparing average nightly prices across NYC's five boroughs. Each bar is color-coded by borough and shows the exact price value."
            )
        else:
            fig_borough = go.Figure()
            fig_borough.add_annotation(
                text="No borough data available<br>Try adjusting your filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="#8b949e"),
                align="center"
            )
            fig_borough.update_layout(
                title='🏙️ Average Price by Borough',
                height=350,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            self.borough_chart.set_figure(fig_borough, is_dark)
        
        # Room Type Distribution
        room_stats = df.groupby('room_type').agg({
            'price': 'mean',
            'id': 'count'
        }).reset_index()
        room_stats.columns = ['Room Type', 'Avg Price', 'Count']
        
        if len(room_stats) > 0:
            # Grayscale-aware colors
            pie_colors = ['#e0e0e0', '#a0a0a0', '#606060'] if self.theme_manager.grayscale_mode else ['#58a6ff', '#3fb950', '#d29922']
            
            fig_room = px.pie(
                room_stats,
                values='Count',
                names='Room Type',
                title='🛏️ Room Type Distribution',
                color_discrete_sequence=pie_colors
            )
            fig_room.update_layout(
                height=380,
                title='🛏️ Room Type Distribution (%)',
            )
            fig_room.update_traces(textposition='inside', textinfo='percent+label')
            self.room_type_chart.set_figure(fig_room, is_dark)
        else:
            fig_room = go.Figure()
            fig_room.add_annotation(
                text="No room type data available<br>Try adjusting your filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="#8b949e"),
                align="center"
            )
            fig_room.update_layout(
                title='🛏️ Room Type Distribution',
                height=350,
                showlegend=False
            )
            self.room_type_chart.set_figure(fig_room, is_dark)
        
        # Value Score Chart (Reviews per Dollar)
        # Always recalculate for consistency with improved formula
        df_value = df.copy()
        df_value['value_score'] = df_value['number_of_reviews'] / (df_value['price'] + 1)
        value_by_borough = df_value.groupby('neighbourhood_group')['value_score'].mean().reset_index()
        value_by_borough.columns = ['Borough', 'Value Score']
        
        if len(value_by_borough) > 0:
            # Grayscale-aware color scale
            value_colorscale = [[0,'#f0f0f0'],[0.5,'#808080'],[1,'#1a1a1a']] if self.theme_manager.grayscale_mode else [[0,'#f0fdf4'],[0.5,'#22c55e'],[1,'#166534']]
            
            fig_value = px.bar(
                value_by_borough.sort_values('Value Score', ascending=True),
                x='Value Score',
                y='Borough',
                orientation='h',
                title='⭐ Value Score by Borough (Reviews/Price)',
                color='Value Score',
                color_continuous_scale=value_colorscale
            )
            fig_value.update_layout(
                height=380,
                showlegend=False,
                xaxis_title='Value Score (Reviews per Dollar)',
                yaxis_title='Borough',
                xaxis=dict(tickformat='.2f')
            )
            self.value_chart.set_figure(fig_value, is_dark)
        else:
            fig_value = go.Figure()
            fig_value.add_annotation(
                text="No value score data available<br>Try adjusting your filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="#8b949e"),
                align="center"
            )
            fig_value.update_layout(
                title='⭐ Value Score by Borough (Reviews/Price)',
                height=350,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            self.value_chart.set_figure(fig_value, is_dark)
        
        # Update Top Value Listings Table
        top_value = self.data_manager.get_top_value_listings(10)
        self.value_table.setRowCount(len(top_value))
        
        for i, (_, row) in enumerate(top_value.iterrows()):
            name = str(row['name'])
            if len(name) > 35:
                name = name[:35] + '...'
            
            self.value_table.setItem(i, 0, QTableWidgetItem(name))
            self.value_table.setItem(i, 1, QTableWidgetItem(str(row['neighbourhood'])))
            
            price_item = QTableWidgetItem(f"${row['price']:.0f}")
            price_item.setForeground(Qt.darkGreen if is_dark else Qt.green)
            self.value_table.setItem(i, 2, price_item)
            
            self.value_table.setItem(i, 3, QTableWidgetItem(f"{row['number_of_reviews']:,.0f}"))
            
            # Add minimum nights column
            min_nights = int(row.get('minimum_nights', 1))
            min_nights_item = QTableWidgetItem(f"{min_nights}")
            # Highlight short stays (good for travelers)
            if min_nights <= 3:
                min_nights_item.setForeground(Qt.darkGreen if is_dark else Qt.green)
            self.value_table.setItem(i, 4, min_nights_item)
            
            self.value_table.setItem(i, 5, QTableWidgetItem(str(row['room_type'])))
            
            score_item = QTableWidgetItem(f"{row['value_score']:.1f}")
            self.value_table.setItem(i, 6, score_item)
    
    def _get_stat_card_colors(self):
        """Get stat card colors based on grayscale mode"""
        if self.theme_manager.grayscale_mode:
            return ["#e0e0e0", "#c0c0c0", "#a0a0a0", "#808080"]
        else:
            return ["#58a6ff", "#3fb950", "#d29922", "#a371f7"]
