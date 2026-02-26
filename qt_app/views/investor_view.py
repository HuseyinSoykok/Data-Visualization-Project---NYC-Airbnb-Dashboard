"""
Investor View - For real estate investors analyzing the market
Enhanced with app_en.py features: violin plots, ROI analysis, segment statistics
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

from qt_app.views.base_view import BaseView
from qt_app.widgets.custom_widgets import ModernCard


class InvestorView(BaseView):
    """View for Investor persona (David)"""
    
    def _setup_content(self):
        # Set header info
        self.persona_badge.setText("🏠 Investor Persona")
        self.title_label.setText("Investment Analysis Dashboard")
        self.desc_label.setText(
            "As David, a real estate investor, analyze market trends and identify "
            "high-yield investment opportunities across NYC's Airbnb market."
        )
        
        # Task info card
        task_card = self.create_info_card(
            "🎯 David's Task",
            "Identify 'Entire home/apt' listings with highest revenue potential using price distribution analysis.\n\n"
            "💡 Focus on: Violin plots show price spread | Box plots reveal outliers | ROI analysis compares segments"
        )
        self.content_layout.addWidget(task_card)
        
        # Stat cards - always colorful (not affected by grayscale mode)
        self.revenue_card = self.add_stat_card("💵", "$0", "Est. Annual Revenue/Listing", "#3fb950")
        self.occupancy_card = self.add_stat_card("📊", "0%", "Avg Availability Rate", "#58a6ff")
        self.hosts_card = self.add_stat_card("👥", "0", "Professional Hosts (10+)", "#d29922")
        self.hotspot_card = self.add_stat_card("🔥", "-", "Hottest Market", "#f85149")
        self.commercial_card = self.add_stat_card("🏢", "0", "Commercial Listings", "#a371f7")
        
        # Charts - Row 1: Revenue Map
        self.revenue_map = self.add_chart(0, 0, 1, 2)
        
        # Row 2: Violin plots for price analysis
        self.violin_borough = self.add_chart(1, 0)
        self.violin_room = self.add_chart(1, 1)
        
        # Row 3: ROI and Host analysis
        self.roi_chart = self.add_chart(2, 0)
        self.host_portfolio = self.add_chart(2, 1)
        
        # Row 4: Market analysis
        self.market_saturation = self.add_chart(3, 0)
        self.yield_analysis = self.add_chart(3, 1)
        
        # Segment Statistics Table
        self._setup_segment_table()
        
        # Top Hosts Table
        self._setup_hosts_table()
        
        # Investment tips
        tips_card = self.create_info_card(
            "📈 Investment Insights",
            "• Entire homes in Manhattan generate highest revenue per listing\n"
            "• Professional hosts (10+ listings) capture 35% of market revenue\n"
            "• Brooklyn shows strong growth potential with lower entry costs\n"
            "• Short-term rentals (1-7 nights) offer higher daily rates\n"
            "• Commercial listings (high availability/many properties) show stable returns"
        )
        self.content_layout.addWidget(tips_card)
    
    def _setup_segment_table(self):
        """Setup segment statistics table"""
        self.segment_card = ModernCard()
        segment_layout = QVBoxLayout(self.segment_card)
        segment_layout.setContentsMargins(16, 16, 16, 16)
        
        header_layout = QHBoxLayout()
        self.segment_title = QLabel("📊 Market Segment Statistics")
        self.segment_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #e6edf3;")
        header_layout.addWidget(self.segment_title)
        header_layout.addStretch()
        segment_layout.addLayout(header_layout)
        
        self.segment_table = QTableWidget()
        self.segment_table.setColumnCount(7)
        self.segment_table.setHorizontalHeaderLabels([
            'Segment', 'Count', 'Avg Price', 'Med Price', 'Std Dev', 'Avg Revenue', 'ROI Score'
        ])
        self.segment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.segment_table.setMinimumHeight(200)
        segment_layout.addWidget(self.segment_table)
        
        self.content_layout.addWidget(self.segment_card)
    
    def _setup_hosts_table(self):
        """Setup top hosts table"""
        self.table_card = ModernCard()
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        
        self.table_title = QLabel("🏆 Top Professional Hosts")
        self.table_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #e6edf3;")
        table_layout.addWidget(self.table_title)
        
        self.hosts_table = QTableWidget()
        self.hosts_table.setColumnCount(5)
        self.hosts_table.setHorizontalHeaderLabels(['Host Name', 'Listings', 'Avg Price', 'Total Reviews', 'Est. Revenue'])
        self.hosts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hosts_table.setMinimumHeight(250)
        table_layout.addWidget(self.hosts_table)
        
        self.content_layout.addWidget(self.table_card)
    
    def _update_table_theme(self, is_dark: bool):
        """Update table theme colors"""
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
        
        table_style = f"""
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
        """
        self.hosts_table.setStyleSheet(table_style)
        self.segment_table.setStyleSheet(table_style)
    
    def refresh(self):
        """Refresh all visualizations with current data"""
        df = self.data_manager.filtered_df
        if df is None or len(df) == 0:
            return
        
        is_dark = self.theme_manager.current_theme == 'dark'
        
        # Update view theme
        self._update_view_theme(is_dark)
        
        # Update table themes
        self._update_table_theme(is_dark)
        
        # Update titles
        title_color = "#e6edf3" if is_dark else "#1f2328"
        card_bg = "#161b22" if is_dark else "#ffffff"
        card_border = "#30363d" if is_dark else "#d0d7de"
        self.table_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {title_color};")
        self.segment_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {title_color};")
        self.table_card.setStyleSheet(f"ModernCard {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 12px; }}")
        self.segment_card.setStyleSheet(f"ModernCard {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 12px; }}")
        
        # Calculate estimated revenue
        df_analysis = df.copy()
        if 'estimated_annual_revenue' in df_analysis.columns:
            df_analysis['estimated_revenue'] = df_analysis['estimated_annual_revenue']
        else:
            df_analysis['estimated_revenue'] = df_analysis['price'] * (365 - df_analysis['availability_365'])
        
        # Update stats
        avg_revenue = df_analysis['estimated_revenue'].mean()
        self.revenue_card.set_value(f"${avg_revenue:,.0f}")
        
        avg_availability = df['availability_365'].mean() / 365 * 100
        self.occupancy_card.set_value(f"{avg_availability:.1f}%")
        
        pro_hosts = df[df['calculated_host_listings_count'] >= 10]['host_id'].nunique()
        self.hosts_card.set_value(f"{pro_hosts:,}")
        
        # Commercial listings
        if 'is_commercial' in df.columns:
            commercial_count = df['is_commercial'].sum()
            self.commercial_card.set_value(f"{commercial_count:,}")
        
        # Hottest market
        market_demand = df.groupby('neighbourhood_group').agg({
            'availability_365': 'mean',
            'number_of_reviews': 'sum'
        }).reset_index()
        market_demand['demand_score'] = market_demand['number_of_reviews'] / (market_demand['availability_365'] + 1)
        hottest = market_demand.loc[market_demand['demand_score'].idxmax(), 'neighbourhood_group']
        self.hotspot_card.set_value(str(hottest))
        
        # Revenue Map with better colorscale (works well in both dark and light mode)
        map_data = self.data_manager.get_map_data(3000)
        map_data['estimated_revenue'] = map_data['price'] * (365 - map_data['availability_365'])
        
        # Grayscale-aware colorscale
        if self.theme_manager.grayscale_mode:
            REVENUE_COLORSCALE = [
                [0, '#f0f0f0'],
                [0.25, '#c0c0c0'],
                [0.5, '#808080'],
                [0.75, '#404040'],
                [1, '#1a1a1a']
            ]
        else:
            REVENUE_COLORSCALE = [
                [0, '#3b82f6'],
                [0.25, '#8b5cf6'],
                [0.5, '#f59e0b'],
                [0.75, '#ef4444'],
                [1, '#dc2626']
            ]
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='latitude',
            lon='longitude',
            color='estimated_revenue',
            size='estimated_revenue',
            size_max=15,
            color_continuous_scale=REVENUE_COLORSCALE,
            hover_name='name',
            hover_data={
                'neighbourhood_group': ':<b>Borough</b>',
                'room_type': True,
                'price': ':$,.0f per night',
                'estimated_revenue': ':$,.0f annual revenue',
                'availability_365': ':.0f days available',
                'number_of_reviews': ':,.0f reviews',
                'latitude': False,
                'longitude': False
            },
            title='💰 Estimated Annual Revenue Distribution',
            zoom=10,
            center=dict(lat=40.7128, lon=-74.0060)
        )
        # Set minimum marker size and transparency for better readability
        fig_map.update_traces(marker=dict(sizemin=3, opacity=0.7))
        fig_map.update_layout(
            mapbox_style='carto-darkmatter' if is_dark else 'carto-positron',
            height=700,
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title=dict(text="Est. Annual Revenue", font=dict(size=12)),
                tickformat="$,.0f",
                tickmode='linear',
                tick0=0,
                dtick=10000,
                thickness=15,
                len=0.6,
                x=1.02,
                xanchor='left'
            ),
            legend=dict(
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
        self.revenue_map.set_figure(fig_map, is_dark)
        
        # Violin Plot - Price by Borough
        df_violin = df_analysis[df_analysis['price'] <= 500]
        
        if len(df_violin) > 0 and df_violin['neighbourhood_group'].nunique() > 0:
            # Grayscale-aware colors
            borough_colors = self._get_borough_colors()
            
            fig_violin_borough = px.violin(
                df_violin,
                x='neighbourhood_group',
                y='price',
                color='neighbourhood_group',
                box=True,
                points='outliers',
                title='Price Distribution by Borough (Violin + Box)',
                labels={'neighbourhood_group': 'Borough', 'price': 'Price ($)'},
                color_discrete_map=borough_colors
            )
            fig_violin_borough.update_layout(
                height=420,
                showlegend=False,
                xaxis_title='Borough',
                yaxis_title='Price per Night (USD)',
                yaxis=dict(tickformat='$,.0f')
            )
            self.violin_borough.set_figure(fig_violin_borough, is_dark)
        else:
            # Empty state with actionable guidance
            fig_violin_borough = go.Figure()
            fig_violin_borough.add_annotation(
                text="<b>Insufficient Data for Analysis</b><br><br>"
                     "📊 Violin plots require data from multiple boroughs<br><br>"
                     "🔧 Solutions:<br>"
                     "• Select 'All' in borough filter<br>"
                     "• Expand your price range<br>"
                     "• Adjust minimum nights filter",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=13, color="#8b949e"),
                align="center"
            )
            fig_violin_borough.update_layout(
                title='Price Distribution by Borough (Violin + Box)',
                height=400,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            self.violin_borough.set_figure(fig_violin_borough, is_dark)
        
        # Violin Plot - Price by Room Type
        if len(df_violin) > 0 and df_violin['room_type'].nunique() > 0:
            # Grayscale-aware colors
            room_colors = self._get_room_type_colors()
            
            fig_violin_room = px.violin(
                df_violin,
                x='room_type',
                y='price',
                color='room_type',
                box=True,
                points='outliers',
                title='Price Distribution by Room Type',
                labels={'room_type': 'Room Type', 'price': 'Price ($)'},
                color_discrete_map=room_colors
            )
            fig_violin_room.update_layout(
                height=420,
                showlegend=False,
                xaxis_title='Room Type',
                yaxis_title='Price per Night (USD)',
                yaxis=dict(tickformat='$,.0f')
            )
            self.violin_room.set_figure(fig_violin_room, is_dark)
        else:
            # Empty state with actionable guidance
            fig_violin_room = go.Figure()
            fig_violin_room.add_annotation(
                text="<b>Insufficient Data for Analysis</b><br><br>"
                     "🏠 Violin plots require data from multiple room types<br><br>"
                     "🔧 Solutions:<br>"
                     "• Select 'All' in room type filter<br>"
                     "• Broaden your search criteria<br>"
                     "• Check other filters aren't too restrictive",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=13, color="#8b949e"),
                align="center"
            )
            fig_violin_room.update_layout(
                title='Price Distribution by Room Type',
                height=400,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            self.violin_room.set_figure(fig_violin_room, is_dark)
        
        # ROI Analysis Chart
        roi_data = self.data_manager.get_roi_data()
        if len(roi_data) > 0:
            # Grayscale-aware colors
            revenue_color = '#808080' if self.theme_manager.grayscale_mode else '#3fb950'
            potential_color = '#404040' if self.theme_manager.grayscale_mode else '#58a6ff'
            
            fig_roi = go.Figure()
            fig_roi.add_trace(go.Bar(
                name='Avg Revenue',
                x=roi_data['room_type'],
                y=roi_data['estimated_annual_revenue'],
                marker_color=revenue_color,
                text=[f'${x:,.0f}' for x in roi_data['estimated_annual_revenue']],
                textposition='auto'
            ))
            fig_roi.add_trace(go.Bar(
                name='Avg Price × 365',
                x=roi_data['room_type'],
                y=roi_data['price'] * 365,
                marker_color=potential_color,
                text=[f'${x:,.0f}' for x in (roi_data['price'] * 365)],
                textposition='auto'
            ))
            fig_roi.update_layout(
                title='📈 ROI Analysis: Revenue vs Potential (by Room Type)',
                barmode='group',
                height=400,
                xaxis_title='Room Type',
                yaxis_title='Amount (USD)',
                yaxis=dict(tickformat='$,.0f'),
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                ),
                annotations=[
                    dict(
                        text='<i>Revenue = Price × Booked Nights (365 - Availability) | Potential = Price × 365</i>',
                        xref='paper', yref='paper',
                        x=0.5, y=-0.12,
                        showarrow=False,
                        font=dict(size=10, color='#8b949e'),
                        xanchor='center'
                    )
                ]
            )
            self.roi_chart.set_figure(fig_roi, is_dark, show_colorbar=False)
        
        # Host Portfolio Analysis - Bar Chart with Enhanced Information
        if 'host_category' in df_analysis.columns:
            # Get detailed host statistics using df_analysis (has estimated_revenue column)
            host_stats = df_analysis.groupby('host_category').agg({
                'id': 'count',
                'estimated_revenue': 'sum',
                'price': 'mean'
            }).reset_index()
            host_stats.columns = ['Category', 'Listings', 'Total Revenue', 'Avg Price']
            
            # Calculate percentages
            total_listings = host_stats['Listings'].sum()
            total_revenue = host_stats['Total Revenue'].sum()
            host_stats['Listings %'] = (host_stats['Listings'] / total_listings * 100).round(1)
            host_stats['Revenue %'] = (host_stats['Total Revenue'] / total_revenue * 100).round(1)
            
            # Sort by number of listings descending
            host_stats = host_stats.sort_values('Listings', ascending=False)
            
            # Category color mapping
            if self.theme_manager.grayscale_mode:
                category_colors = {
                    'Single (1)': '#e0e0e0',
                    'Small (2-5)': '#a0a0a0',
                    'Medium (6-10)': '#606060',
                    'Mega (10+)': '#1a1a1a'
                }
            else:
                category_colors = {
                    'Single (1)': '#58a6ff',
                    'Small (2-5)': '#3fb950',
                    'Medium (6-10)': '#d29922',
                    'Mega (10+)': '#f85149'
                }
            
            fig_portfolio = px.bar(
                host_stats,
                x='Category',
                y='Listings',
                color='Category',
                color_discrete_map=category_colors,
                title='👥 Market Distribution by Host Category',
                text='Listings'
            )
            
            # Add count and percentage to text
            fig_portfolio.update_traces(
                texttemplate='%{text:,}<br>(%{customdata[0]:.1f}%)<br>$%{customdata[1]:,.0f}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                             'Listings: %{y:,} (%{customdata[0]:.1f}%)<br>' +
                             'Total Revenue: $%{customdata[1]:,.0f} (%{customdata[2]:.1f}%)<br>' +
                             'Avg Price: $%{customdata[3]:.0f}<br>' +
                             '<extra></extra>',
                customdata=host_stats[['Listings %', 'Total Revenue', 'Revenue %', 'Avg Price']]
            )
            
            fig_portfolio.update_layout(
                height=400,
                showlegend=False,
                xaxis_title='Host Category',
                yaxis_title='Number of Listings',
                yaxis=dict(tickformat=',d'),
                annotations=[
                    dict(
                        text='<i>💡 Format: Count (% of total) | Total Revenue<br>' +
                             'Mega hosts (10+ listings) often dominate revenue despite fewer total listings</i>',
                        xref='paper', yref='paper',
                        x=0.5, y=-0.18,
                        showarrow=False,
                        font=dict(size=10, color='#8b949e'),
                        xanchor='center'
                    )
                ]
            )
        else:
            # Fallback using host_size with df_analysis (has estimated_revenue column)
            host_sizes = df_analysis.groupby('host_size').agg({
                'id': 'count',
                'estimated_revenue': 'sum'
            }).reset_index()
            host_sizes.columns = ['Host Size', 'Listings', 'Total Revenue']
            
            # Calculate percentages
            total_listings = host_sizes['Listings'].sum()
            host_sizes['Percentage'] = (host_sizes['Listings'] / total_listings * 100).round(1)
            host_sizes = host_sizes.sort_values('Listings', ascending=False)
            
            # Grayscale-aware colors
            bar_colors = ['#e0e0e0', '#a0a0a0', '#606060', '#1a1a1a'] if self.theme_manager.grayscale_mode else ['#58a6ff', '#3fb950', '#d29922', '#f85149']
            
            fig_portfolio = px.bar(
                host_sizes,
                x='Host Size',
                y='Listings',
                color='Host Size',
                color_discrete_sequence=bar_colors,
                title='👥 Market Distribution by Host Size',
                text='Listings'
            )
            
            fig_portfolio.update_traces(
                texttemplate='%{text:,}<br>(%{customdata:.1f}%)',
                textposition='outside',
                customdata=host_sizes['Percentage']
            )
            
            fig_portfolio.update_layout(
                height=400,
                showlegend=False,
                xaxis_title='Host Size',
                yaxis_title='Number of Listings',
                yaxis=dict(tickformat=',d')
            )
        
        self.host_portfolio.set_figure(fig_portfolio, is_dark, show_colorbar=False)
        
        # Market Saturation
        saturation = df.groupby('neighbourhood_group').agg({
            'id': 'count',
            'availability_365': 'mean'
        }).reset_index()
        saturation.columns = ['Borough', 'Listings', 'Avg Availability']
        
        # Grayscale-aware borough colors
        borough_colors = self._get_borough_colors()
        
        fig_saturation = go.Figure()
        
        median_availability = saturation['Avg Availability'].median()
        
        for borough in saturation['Borough'].unique():
            borough_data = saturation[saturation['Borough'] == borough]
            fig_saturation.add_trace(go.Scatter(
                x=borough_data['Listings'],
                y=borough_data['Avg Availability'],
                mode='markers',
                name=borough,
                marker=dict(
                    size=25,  # Fixed size for all markers
                    color=borough_colors.get(borough, '#8b949e'),
                    line=dict(width=1, color='rgba(255,255,255,0.3)')
                ),
                hovertemplate=f'<b>{borough}</b><br>Listings: %{{x:,.0f}}<br>Avg Availability: %{{y:.0f}} days<extra></extra>'
            ))
        
        # Add median availability line
        fig_saturation.add_hline(
            y=median_availability,
            line_dash="dash",
            line_color="#8b949e",
            annotation_text=f"Median Availability: {median_availability:.0f} days",
            annotation_position="top right"
        )
        
        fig_saturation.update_layout(
            title='🎯 Market Saturation Analysis',
            xaxis_title='Number of Listings',
            yaxis_title='Average Availability (Days per Year)',
            height=400,
            showlegend=True,
            xaxis=dict(tickformat=',d'),
            yaxis=dict(tickformat='.0f'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            annotations=[
                dict(
                    text='<i>💡 Investment Guide: High listings + Low availability = High demand (Ideal)<br>'
                         'High listings + High availability = Oversaturated market (Risk)</i>',
                    xref='paper', yref='paper',
                    x=0.5, y=-0.15,
                    showarrow=False,
                    font=dict(size=10, color='#8b949e'),
                    xanchor='center'
                )
            ]
        )
        self.market_saturation.set_figure(fig_saturation, is_dark, show_colorbar=False)
        
        # Yield Analysis by Borough
        yield_data = df_analysis.groupby('neighbourhood_group').agg({
            'estimated_revenue': 'mean',
            'price': 'mean'
        }).reset_index()
        yield_data['yield_ratio'] = yield_data['estimated_revenue'] / (yield_data['price'] * 365) * 100
        
        # Grayscale-aware color scale
        yield_colorscale = [[0,'#f0f0f0'],[0.5,'#808080'],[1,'#1a1a1a']] if self.theme_manager.grayscale_mode else [[0,'#fff7ed'],[0.5,'#f97316'],[1,'#9a3412']]
        
        fig_yield = px.bar(
            yield_data.sort_values('yield_ratio', ascending=True),
            x='yield_ratio',
            y='neighbourhood_group',
            orientation='h',
            title='📈 Investment Yield by Borough (%)',
            color='yield_ratio',
            color_continuous_scale=yield_colorscale,
            labels={'yield_ratio': 'Yield (%)', 'neighbourhood_group': 'Borough'},
            text='yield_ratio'
        )
        fig_yield.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig_yield.update_layout(
            height=400,
            showlegend=False,
            xaxis_title='Yield Percentage (%)',
            yaxis_title='Borough',
            xaxis=dict(tickformat='.1f')
        )
        self.yield_analysis.set_figure(fig_yield, is_dark)
        
        # Update Segment Statistics Table
        segments = df_analysis.groupby('room_type').agg({
            'id': 'count',
            'price': ['mean', 'median', 'std'],
            'estimated_revenue': 'mean'
        }).reset_index()
        segments.columns = ['Segment', 'Count', 'Avg Price', 'Med Price', 'Std Dev', 'Avg Revenue']
        # ROI Score: actual revenue as % of max potential (price × 365)
        segments['ROI Score'] = (segments['Avg Revenue'] / (segments['Avg Price'] * 365) * 100).round(1)
        
        self.segment_table.setRowCount(len(segments))
        for i, row in segments.iterrows():
            self.segment_table.setItem(i, 0, QTableWidgetItem(str(row['Segment'])))
            self.segment_table.setItem(i, 1, QTableWidgetItem(f"{row['Count']:,}"))
            self.segment_table.setItem(i, 2, QTableWidgetItem(f"${row['Avg Price']:.0f}"))
            self.segment_table.setItem(i, 3, QTableWidgetItem(f"${row['Med Price']:.0f}"))
            self.segment_table.setItem(i, 4, QTableWidgetItem(f"${row['Std Dev']:.0f}"))
            self.segment_table.setItem(i, 5, QTableWidgetItem(f"${row['Avg Revenue']:,.0f}"))
            self.segment_table.setItem(i, 6, QTableWidgetItem(f"{row['ROI Score']:.1f}%"))
        
        # Update hosts table
        top_hosts = self.data_manager.get_top_hosts(10)
        if len(top_hosts) > 0:
            self.hosts_table.setRowCount(len(top_hosts))
            for idx, (i, row) in enumerate(top_hosts.iterrows()):
                self.hosts_table.setItem(idx, 0, QTableWidgetItem(str(row['host_name'])))
                self.hosts_table.setItem(idx, 1, QTableWidgetItem(str(row['listing_count'])))
                self.hosts_table.setItem(idx, 2, QTableWidgetItem(f"${row['avg_price']:.0f}"))
                self.hosts_table.setItem(idx, 3, QTableWidgetItem(str(int(row['total_reviews']))))
                est_rev = row['avg_price'] * 200 * row['listing_count']  # Rough estimate
                self.hosts_table.setItem(idx, 4, QTableWidgetItem(f"${est_rev:,.0f}"))
        else:
            self.hosts_table.setRowCount(0)
    
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
                'Brooklyn': '#3b82f6',
                'Queens': '#10b981',
                'Bronx': '#ef4444',
                'Staten Island': '#8b5cf6'
            }
    
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
