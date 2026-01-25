"""
Journalist View - For data journalists and researchers
Enhanced with app_en.py features: host distribution histogram, pie chart, temporal trend
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

from qt_app.views.base_view import BaseView
from qt_app.widgets.custom_widgets import ModernCard


class JournalistView(BaseView):
    """View for Journalist persona (Michael) - Data Journalism"""
    
    def _setup_content(self):
        # Set header info
        self.persona_badge.setText("📰 Journalist Persona")
        self.title_label.setText("Data Story Explorer")
        self.desc_label.setText(
            "As Michael, a data journalist, uncover compelling stories in NYC's Airbnb data. "
            "Find patterns, outliers, and trends that tell the story of short-term rentals."
        )
        
        # Task info card
        task_card = self.create_info_card(
            "🎯 Michael's Task",
            "Identify host distribution patterns and market concentration for investigative reporting.\n\n"
            "💡 Key insight: The histogram shows how many hosts own how many listings - revealing 'power hosts'"
        )
        self.content_layout.addWidget(task_card)
        
        # Stat cards - always colorful (not affected by grayscale mode)
        self.total_card = self.add_stat_card("📊", "0", "Total Listings Analyzed", "#58a6ff")
        self.hosts_card = self.add_stat_card("👥", "0", "Unique Hosts", "#3fb950")
        self.concentration_card = self.add_stat_card("📈", "0%", "Top 1% Host Control", "#f85149")
        self.reviews_card = self.add_stat_card("⭐", "0M", "Total Reviews", "#d29922")
        self.commercial_card = self.add_stat_card("🏢", "0", "Commercial Operators", "#a371f7")
        
        # Charts - Row 1: Overview Map
        self.overview_map = self.add_chart(0, 0, 1, 2)
        
        # Row 2: Host Distribution Histogram + Pie Chart
        self.host_histogram = self.add_chart(1, 0)
        self.host_category_pie = self.add_chart(1, 1)
        
        # Row 3: Inequality + Temporal Trend
        self.inequality_chart = self.add_chart(2, 0)
        self.temporal_trend = self.add_chart(2, 1)
        
        # Row 4: Borough profiles
        self.neighbourhood_story = self.add_chart(3, 0)
        self.price_inequality = self.add_chart(3, 1)
        
        # Key Data Points Table
        self._setup_data_points_table()
        
        # Story angles
        stories_card = self.create_info_card(
            "📝 Story Angles",
            "• 'The Airbnb Empire Builders': Top hosts control X% of listings\n"
            "• 'Neighborhood Transformation': How Airbnb reshapes communities\n"
            "• 'The Price Divide': Luxury listings vs affordable stays\n"
            "• 'Hidden Hotels': Commercial operators disguised as hosts\n"
            "• 'The Availability Paradox': Always-vacant listings"
        )
        self.content_layout.addWidget(stories_card)
        
        # Data sources
        sources_card = self.create_info_card(
            "📚 Data Notes",
            "• Dataset: Inside Airbnb NYC 2019\n"
            "• Coverage: All 5 NYC boroughs\n"
            "• Metrics: Price, availability, reviews, host data\n"
            "• Limitations: Point-in-time snapshot, self-reported data\n"
            "• Source: insideairbnb.com (open data)"
        )
        self.content_layout.addWidget(sources_card)
    
    def _setup_data_points_table(self):
        """Setup key data points table for quick headlines"""
        self.data_card = ModernCard()
        data_layout = QVBoxLayout(self.data_card)
        data_layout.setContentsMargins(16, 16, 16, 16)
        
        header_layout = QHBoxLayout()
        self.data_title = QLabel("📰 Key Data Points for Headlines")
        self.data_title.setObjectName("data_table_title")
        self.data_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #e6edf3;")
        header_layout.addWidget(self.data_title)
        header_layout.addStretch()
        data_layout.addLayout(header_layout)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(['Metric', 'Value', 'Context'])
        self.data_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.data_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.data_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.data_table.setMinimumHeight(250)
        data_layout.addWidget(self.data_table)
        
        self.content_layout.addWidget(self.data_card)
    
    def _update_table_theme(self, is_dark: bool):
        """Update table theme"""
        if is_dark:
            bg_color = '#0d1117'
            header_bg = '#161b22'
            text_color = '#e6edf3'
            border_color = '#21262d'
        else:
            bg_color = '#ffffff'
            header_bg = '#f6f8fa'
            text_color = '#1f2328'
            border_color = '#d0d7de'
        
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                gridline-color: {border_color};
                color: {text_color};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {border_color};
                color: {text_color};
            }}
            QHeaderView::section {{
                background-color: {header_bg};
                color: {text_color};
                padding: 10px;
                border: none;
                font-weight: 600;
            }}
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
        
        # Update stats
        total_listings = len(df)
        self.total_card.set_value(f"{total_listings:,}")
        
        unique_hosts = df['host_id'].nunique()
        self.hosts_card.set_value(f"{unique_hosts:,}")
        
        # Top 1% host concentration
        host_counts = df['host_id'].value_counts()
        top_1_pct_threshold = max(1, int(len(host_counts) * 0.01))
        top_hosts_listings = host_counts.head(top_1_pct_threshold).sum()
        concentration = top_hosts_listings / total_listings * 100
        self.concentration_card.set_value(f"{concentration:.1f}%")
        
        total_reviews = df['number_of_reviews'].sum()
        reviews_display = f"{total_reviews/1e6:.1f}M" if total_reviews > 1e6 else f"{total_reviews/1e3:.0f}K"
        self.reviews_card.set_value(reviews_display)
        
        # Commercial operators
        if 'is_commercial' in df.columns:
            commercial_count = df[df['is_commercial'] == True]['host_id'].nunique()
            self.commercial_card.set_value(f"{commercial_count:,}")
        
        # Overview Map
        map_data = self.data_manager.get_map_data(4000)
        
        # Grayscale-aware borough colors
        borough_color_map = self._get_borough_colors()
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='latitude',
            lon='longitude',
            color='neighbourhood_group',
            color_discrete_map=borough_color_map,
            hover_name='name',
            hover_data={
                'price': ':$,.0f per night',
                'room_type': True,
                'neighbourhood': True,
                'number_of_reviews': ':,.0f reviews',
                'host_name': ':<b>Host</b>',
                'availability_365': ':.0f days available',
                'latitude': False,
                'longitude': False
            },
            title='🗺️ NYC Airbnb Landscape - The Big Picture',
            zoom=10,
            center=dict(lat=40.7128, lon=-74.0060),
            opacity=0.7
        )
        # Set consistent marker size for better visibility
        fig_map.update_traces(marker=dict(size=10))
        fig_map.update_layout(
            mapbox_style='carto-darkmatter' if is_dark else 'carto-positron',
            height=700,
            margin=dict(l=0, r=0, t=50, b=0),
            legend=dict(
                title=dict(text="Borough", font=dict(size=12, color='#e6edf3' if is_dark else '#1f2328')),
                orientation='v',
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=0.01,
                bgcolor='rgba(0,0,0,0.7)' if is_dark else 'rgba(255,255,255,0.9)',
                bordercolor='#30363d' if is_dark else '#d0d7de',
                borderwidth=1,
                font=dict(color='#e6edf3' if is_dark else '#1f2328')
            )
        )
        self.overview_map.set_figure(fig_map, is_dark, show_colorbar=False)
        
        # Host Distribution Histogram (like app_en.py)
        host_listing_counts = df['host_id'].value_counts().reset_index()
        host_listing_counts.columns = ['host_id', 'listing_count']
        
        # Bin the data
        bins = [1, 2, 3, 5, 10, 20, 50, 100, np.inf]
        labels = ['1', '2', '3-4', '5-9', '10-19', '20-49', '50-99', '100+']
        host_listing_counts['bin'] = pd.cut(host_listing_counts['listing_count'], bins=bins, labels=labels, right=False)
        bin_counts = host_listing_counts['bin'].value_counts().reindex(labels).fillna(0)
        marker_color = '#808080' if self.theme_manager.grayscale_mode else '#58a6ff'
        
        fig_histogram = go.Figure()
        fig_histogram.add_trace(go.Bar(
            x=labels,
            y=bin_counts.values,
            marker_color=marker_color,
            text=[f'{int(val):,}' for val in bin_counts.values],
            textposition='auto',
            textfont=dict(size=11)
        ))
        fig_histogram.update_layout(
            title='📊 Host Distribution: Number of Listings per Host',
            xaxis_title='Number of Listings Owned',
            yaxis_title='Number of Hosts',
            height=400,
            xaxis=dict(type='category'),
            yaxis=dict(tickformat=',d')
        )
        self.host_histogram.set_figure(fig_histogram, is_dark, show_colorbar=False)
        
        # Host Category Pie Chart
        pie_colors = ['#e0e0e0', '#c0c0c0', '#a0a0a0', '#808080'] if self.theme_manager.grayscale_mode else ['#58a6ff', '#3fb950', '#d29922', '#f85149']
        
        if 'host_category' in df.columns:
            host_stats = self.data_manager.get_host_category_stats()
            fig_pie = px.pie(
                host_stats,
                values='count',
                names='host_category',
                title='👥 Host Categories Distribution',
                color_discrete_sequence=pie_colors
            )
        else:
            # Fallback to host_size
            host_sizes = df.groupby('host_size')['id'].count().reset_index()
            host_sizes.columns = ['Category', 'Count']
            fig_pie = px.pie(
                host_sizes,
                values='Count',
                names='Category',
                title='👥 Host Size Distribution',
                color_discrete_sequence=pie_colors
            )
        fig_pie.update_layout(height=400)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        self.host_category_pie.set_figure(fig_pie, is_dark)
        
        # Host Inequality - Lorenz-like curve
        host_listings = df['host_id'].value_counts().sort_values()
        cumulative_listings = host_listings.cumsum()
        
        sample_size = min(1000, len(host_listings))
        indices = [int(i * len(host_listings) / sample_size) for i in range(sample_size)]
        
        # Grayscale-aware colors
        actual_color = '#606060' if self.theme_manager.grayscale_mode else '#f85149'
        equality_color = '#a0a0a0' if self.theme_manager.grayscale_mode else '#3fb950'
        fill_color = 'rgba(96, 96, 96, 0.2)' if self.theme_manager.grayscale_mode else 'rgba(248, 81, 73, 0.2)'
        
        fig_inequality = go.Figure()
        fig_inequality.add_trace(go.Scatter(
            x=[i/len(host_listings)*100 for i in indices],
            y=[cumulative_listings.iloc[i]/total_listings*100 for i in indices],
            mode='lines',
            name='Actual Distribution',
            line=dict(color=actual_color, width=3),
            fill='tozeroy',
            fillcolor=fill_color
        ))
        fig_inequality.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            name='Perfect Equality',
            line=dict(color=equality_color, dash='dash', width=2)
        ))
        fig_inequality.update_layout(
            title='📈 Host Concentration: Who Controls the Market?',
            xaxis_title='Cumulative % of Hosts (ordered by portfolio size)',
            yaxis_title='Cumulative % of Total Listings',
            height=400,
            xaxis=dict(tickformat='.0f', ticksuffix='%'),
            yaxis=dict(tickformat='.0f', ticksuffix='%'),
            annotations=[
                dict(
                    text='<i>Data source: NYC Airbnb 2019 | Area between curves shows inequality</i>',
                    xref='paper', yref='paper',
                    x=0.5, y=-0.15,
                    showarrow=False,
                    font=dict(size=10, color='#8b949e'),
                    xanchor='center'
                )
            ]
        )
        self.inequality_chart.set_figure(fig_inequality, is_dark)
        
        # Temporal Trend (Monthly Reviews - proxy for activity)
        monthly_trend = self.data_manager.get_monthly_review_trend()
        if monthly_trend is not None and len(monthly_trend) > 0:
            fig_trend = px.line(
                monthly_trend,
                x='review_month',
                y='count',
                title='📅 Monthly Review Activity Trend',
                labels={'review_month': 'Month', 'count': 'Reviews'},
                markers=True
            )
            line_color = '#808080' if self.theme_manager.grayscale_mode else '#58a6ff'
            fig_trend.update_traces(line_color=line_color, line_width=3)
            fig_trend.update_layout(
                height=400,
                xaxis_title='Review Month',
                yaxis_title='Number of Reviews',
                yaxis=dict(tickformat=',d')
            )
            self.temporal_trend.set_figure(fig_trend, is_dark, show_colorbar=False)
        else:
            # Fallback - reviews by last review date
            if 'last_review_month' in df.columns:
                monthly = df.groupby('last_review_month')['number_of_reviews'].sum().reset_index()
                monthly.columns = ['Month', 'Reviews']
                fig_trend = px.bar(
                    monthly.sort_values('Month'),
                    x='Month',
                    y='Reviews',
                    title='📅 Review Activity by Month',
                    color_discrete_sequence=['#58a6ff']
                )
            else:
                review_dist = df.groupby('neighbourhood_group')['number_of_reviews'].sum().reset_index()
                fig_trend = px.bar(
                    review_dist,
                    x='neighbourhood_group',
                    y='number_of_reviews',
                    title='📅 Total Reviews by Borough',
                    color_discrete_sequence=['#58a6ff']
                )
            fig_trend.update_layout(height=400)
        self.temporal_trend.set_figure(fig_trend, is_dark, show_colorbar=False)
        
        # Neighbourhood Story - Character of each borough
        borough_profile = df.groupby('neighbourhood_group').agg({
            'price': ['mean', 'median'],
            'id': 'count',
            'number_of_reviews': 'mean',
            'availability_365': 'mean'
        }).reset_index()
        borough_profile.columns = ['Borough', 'Mean Price', 'Median Price', 'Listings', 'Avg Reviews', 'Avg Availability']
        
        # Grayscale-aware colors
        price_color = '#808080' if self.theme_manager.grayscale_mode else '#58a6ff'
        reviews_color = '#404040' if self.theme_manager.grayscale_mode else '#3fb950'
        
        # Borough Profile - Radar chart showing multiple dimensions
        fig_borough = go.Figure()
        fig_borough.add_trace(go.Scatterpolar(
            r=[borough_profile[borough_profile['Borough'] == b]['Mean Price'].values[0] for b in borough_profile['Borough']],
            theta=borough_profile['Borough'],
            fill='toself',
            name='Mean Price',
            line_color=price_color
        ))
        fig_borough.add_trace(go.Scatterpolar(
            r=[borough_profile[borough_profile['Borough'] == b]['Avg Reviews'].values[0] * 5 for b in borough_profile['Borough']],
            theta=borough_profile['Borough'],
            fill='toself',
            name='Avg Reviews (scaled)',
            line_color=reviews_color
        ))
        fig_borough.update_layout(
            title='🏙️ Borough Personality Profiles',
            polar=dict(radialaxis=dict(visible=True)),
            height=400,
            annotations=[
                dict(
                    text='<i>💡 Multi-dimensional borough analysis: Price levels and review activity combined<br>'
                         'Larger area = More expensive with higher engagement</i>',
                    xref='paper', yref='paper',
                    x=0.5, y=-0.1,
                    showarrow=False,
                    font=dict(size=10, color='#8b949e'),
                    xanchor='center'
                )
            ]
        )
        self.neighbourhood_story.set_figure(fig_borough, is_dark, show_colorbar=False)
        
        # Price Inequality by Borough
        df_price_filtered = df[df['price'] <= 500]
        q25 = df_price_filtered['price'].quantile(0.25)
        q75 = df_price_filtered['price'].quantile(0.75)
        
        # Grayscale-aware borough colors
        borough_colors = self._get_borough_colors()
        
        fig_price_ineq = px.violin(
            df_price_filtered,
            x='neighbourhood_group',
            y='price',
            color='neighbourhood_group',
            color_discrete_map=borough_colors,
            title='💰 Price Inequality Across Boroughs',
            box=True,
            points='outliers'
        )
        # Add quartile lines
        fig_price_ineq.add_hline(
            y=q25,
            line_dash="dash",
            line_color="#8b949e",
            annotation_text=f"Q1: ${q25:.0f}",
            annotation_position="left"
        )
        fig_price_ineq.add_hline(
            y=q75,
            line_dash="dash",
            line_color="#8b949e",
            annotation_text=f"Q3: ${q75:.0f}",
            annotation_position="right"
        )
        fig_price_ineq.update_layout(
            height=400,
            showlegend=False,
            xaxis_title='Borough',
            yaxis_title='Price per Night (USD)',
            yaxis=dict(tickformat='$,.0f')
        )
        self.price_inequality.set_figure(fig_price_ineq, is_dark)
        
        # Update Key Data Points Table
        data_points = [
            ("Total Listings", f"{total_listings:,}", "Active listings in filtered data"),
            ("Unique Hosts", f"{unique_hosts:,}", f"Avg {total_listings/unique_hosts:.1f} listings per host"),
            ("Top 1% Control", f"{concentration:.1f}%", "Market concentration metric"),
            ("Total Reviews", reviews_display, "Proxy for total bookings"),
            ("Avg Price", f"${df['price'].mean():.0f}", f"Median: ${df['price'].median():.0f}"),
            ("Price Range", f"${df['price'].min():.0f} - ${df['price'].max():.0f}", "Min to max price"),
            ("Most Common Type", df['room_type'].mode().iloc[0] if len(df['room_type'].mode()) > 0 else "N/A", 
             f"{(df['room_type'].value_counts().iloc[0]/len(df)*100):.1f}% of listings"),
            ("Top Borough", df['neighbourhood_group'].mode().iloc[0] if len(df['neighbourhood_group'].mode()) > 0 else "N/A",
             f"{(df['neighbourhood_group'].value_counts().iloc[0]/len(df)*100):.1f}% of listings"),
        ]
        
        self.data_table.setRowCount(len(data_points))
        for i, (metric, value, context) in enumerate(data_points):
            self.data_table.setItem(i, 0, QTableWidgetItem(metric))
            self.data_table.setItem(i, 1, QTableWidgetItem(value))
            self.data_table.setItem(i, 2, QTableWidgetItem(context))    
    def _get_borough_colors(self):
        """Get borough colors based on grayscale mode"""
        if self.theme_manager.grayscale_mode:
            return {
                'Manhattan': '#1a1a1a',
                'Brooklyn': '#404040',
                'Queens': '#666666',
                'Bronx': '#8c8c8c',
                'Staten Island': '#b3b3b3'
            }
        else:
            return {
                'Manhattan': '#f59e0b',
                'Brooklyn': '#ef4444',
                'Queens': '#10b981',
                'Bronx': '#3b82f6',
                'Staten Island': '#8b5cf6'
            }