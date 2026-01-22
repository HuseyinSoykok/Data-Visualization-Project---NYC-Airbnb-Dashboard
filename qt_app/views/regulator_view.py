"""
Regulator View - For policy makers and city regulators
Enhanced with app_en.py features: commercial vs regular comparison, density heatmap
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

from qt_app.views.base_view import BaseView
from qt_app.widgets.custom_widgets import ModernCard, Badge


class RegulatorView(BaseView):
    """View for Regulator persona (Dr. Chen)"""
    
    def _setup_content(self):
        # Set header info  
        self.persona_badge.setText("📋 Regulator Persona")
        self.title_label.setText("Regulatory Compliance Dashboard")
        self.desc_label.setText(
            "As Dr. Chen, a city housing regulator, monitor short-term rental compliance, "
            "identify potential violations, and analyze the impact on housing availability."
        )
        
        # Task info card
        task_card = self.create_info_card(
            "🎯 Dr. Chen's Task",
            "Identify and analyze commercial short-term rental operations for regulatory oversight.\n\n"
            "💡 Commercial = high availability (>300 days) OR many listings (>5) per host"
        )
        self.content_layout.addWidget(task_card)
        
        # Stat cards
        self.illegal_card = self.add_stat_card("⚠️", "0", "Potential Violations (>30 nights)", "#f85149")
        self.commercial_card = self.add_stat_card("🏢", "0", "Commercial Listings", "#d29922")
        self.unlicensed_card = self.add_stat_card("📝", "0%", "High Availability Listings", "#58a6ff")
        self.impact_card = self.add_stat_card("🏘️", "0", "Listings Removing Housing", "#a371f7")
        self.compliance_card = self.add_stat_card("✅", "0%", "Compliance Rate", "#3fb950")
        
        # Charts - Row 1: Violation Map
        self.violation_map = self.add_chart(0, 0, 1, 2)
        
        # Row 2: Min nights + Commercial density
        self.min_nights_chart = self.add_chart(1, 0)
        self.commercial_density = self.add_chart(1, 1)
        
        # Row 3: Borough violations + Availability
        self.borough_violations = self.add_chart(2, 0)
        self.availability_analysis = self.add_chart(2, 1)
        
        # Commercial vs Regular Comparison Table
        self._setup_comparison_table()
        
        # Policy recommendations
        policy_card = self.create_info_card(
            "📜 Policy Recommendations",
            "• Enforce 30-day minimum stay for entire home rentals\n"
            "• Cap individual hosts at maximum 3 listings\n"
            "• Require registration for all short-term rentals\n"
            "• Increase inspections in Manhattan and Brooklyn\n"
            "• Create affordable housing offset requirements"
        )
        self.content_layout.addWidget(policy_card)
        
        # Compliance metrics
        compliance_card = self.create_info_card(
            "📊 Compliance Metrics",
            "NYC Local Law 18 requires:\n"
            "• Host must be present during rental (entire apt)\n"
            "• Maximum 2 guests for shared accommodations\n"
            "• Registration with city required\n"
            "• Building rules must permit short-term rentals"
        )
        self.content_layout.addWidget(compliance_card)
    
    def _setup_comparison_table(self):
        """Setup commercial vs regular comparison table"""
        self.comparison_card = ModernCard()
        comparison_layout = QVBoxLayout(self.comparison_card)
        comparison_layout.setContentsMargins(16, 16, 16, 16)
        
        header_layout = QHBoxLayout()
        self.comparison_title = QLabel("📊 Commercial vs Regular Listings Comparison")
        self.comparison_title.setObjectName("comparison_title")
        self.comparison_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #e6edf3;")
        header_layout.addWidget(self.comparison_title)
        header_layout.addStretch()
        comparison_layout.addLayout(header_layout)
        
        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(4)
        self.comparison_table.setHorizontalHeaderLabels(['Metric', 'Commercial', 'Regular', 'Difference'])
        self.comparison_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.comparison_table.setMinimumHeight(300)
        comparison_layout.addWidget(self.comparison_table)
        
        self.content_layout.addWidget(self.comparison_card)
    
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
        
        self.comparison_table.setStyleSheet(f"""
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
        
        # Calculate violation metrics
        df_violations = df[(df['room_type'] == 'Entire home/apt') & (df['minimum_nights'] < 30)]
        violations_count = len(df_violations)
        self.illegal_card.set_value(f"{violations_count:,}")
        
        # Commercial listings (using is_commercial flag or fallback)
        if 'is_commercial' in df.columns:
            commercial_count = df['is_commercial'].sum()
            df_commercial = df[df['is_commercial'] == True]
            df_regular = df[df['is_commercial'] == False]
        else:
            df_commercial = df[(df['availability_365'] > 300) | (df['calculated_host_listings_count'] > 5)]
            df_regular = df[(df['availability_365'] <= 300) & (df['calculated_host_listings_count'] <= 5)]
            commercial_count = len(df_commercial)
        
        self.commercial_card.set_value(f"{commercial_count:,}")
        
        # High availability
        high_availability = len(df[df['availability_365'] > 270])
        high_avail_pct = high_availability / len(df) * 100 if len(df) > 0 else 0
        self.unlicensed_card.set_value(f"{high_avail_pct:.1f}%")
        
        # Listings removing housing
        housing_impact = len(df[(df['room_type'] == 'Entire home/apt') & (df['availability_365'] > 180)])
        self.impact_card.set_value(f"{housing_impact:,}")
        
        # Compliance rate (listings NOT violating)
        compliant = len(df) - violations_count
        compliance_rate = compliant / len(df) * 100 if len(df) > 0 else 0
        self.compliance_card.set_value(f"{compliance_rate:.1f}%")
        
        # Violation Map with heatmap-style density
        map_data = df_violations.sample(n=min(2000, len(df_violations)), random_state=42) if len(df_violations) > 2000 else df_violations
        
        if len(map_data) > 0:
            # Enhanced colorbar colors for dark/light mode
            colorbar_text = '#e6edf3' if is_dark else '#1f2328'
            
            fig_map = px.density_mapbox(
                map_data,
                lat='latitude',
                lon='longitude',
                radius=15,
                zoom=10,
                center=dict(lat=40.7128, lon=-74.0060),
                title='⚠️ Violation Density Heatmap (Entire Homes, Min Stay < 30)',
                color_continuous_scale=[
                    [0.0, '#fef0d9'],   # Light yellow (low density)
                    [0.3, '#fdcc8a'],   # Orange
                    [0.6, '#fc8d59'],   # Dark orange
                    [0.8, '#e34a33'],   # Red
                    [1.0, '#b30000']    # Dark red (high density)
                ]
            )
            fig_map.update_layout(
                mapbox_style='carto-darkmatter' if is_dark else 'carto-positron',
                height=700,
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_colorbar=dict(
                    title=dict(text="Violation Density", font=dict(color=colorbar_text, size=12)),
                    tickfont=dict(color=colorbar_text, size=10),
                    thickness=15,
                    len=0.7,
                    x=1.02,
                    xanchor='left',
                    bgcolor='rgba(0,0,0,0)',
                    outlinewidth=0,
                    tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                    ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High']
                ),
                annotations=[
                    dict(
                        text='<i>Shows concentration of entire home listings with <30 night minimum (potential violations)</i>',
                        xref='paper', yref='paper',
                        x=0.5, y=0.01,
                        showarrow=False,
                        font=dict(size=10, color=colorbar_text),
                        xanchor='center',
                        bgcolor='rgba(0,0,0,0.5)' if is_dark else 'rgba(255,255,255,0.8)',
                        borderpad=5
                    )
                ]
            )
            self.violation_map.set_figure(fig_map, is_dark)
        
        # Minimum Nights Distribution
        fig_nights = px.histogram(
            df[df['minimum_nights'] <= 90],
            x='minimum_nights',
            nbins=30,
            title='📅 Minimum Nights Distribution',
            labels={'minimum_nights': 'Minimum Nights Required'},
            color_discrete_sequence=['#f85149']
        )
        fig_nights.add_vline(x=30, line_dash="dash", line_color="#3fb950", 
                            annotation_text="Legal 30-day threshold", annotation_position="top right")
        fig_nights.update_layout(
            height=420,
            xaxis_title='Minimum Nights Required',
            yaxis_title='Number of Listings',
            xaxis=dict(tickformat=',d'),
            yaxis=dict(tickformat=',d')
        )
        self.min_nights_chart.set_figure(fig_nights, is_dark, show_colorbar=False)
        
        # Commercial Density by Borough
        if 'is_commercial' in df.columns:
            commercial_by_borough = df.groupby('neighbourhood_group').agg({
                'is_commercial': ['sum', 'count']
            }).reset_index()
            commercial_by_borough.columns = ['Borough', 'Commercial', 'Total']
            commercial_by_borough['Commercial %'] = commercial_by_borough['Commercial'] / commercial_by_borough['Total'] * 100
            
            fig_density = px.bar(
                commercial_by_borough,
                x='Borough',
                y='Commercial %',
                title='🏢 Commercial Listing Rate by Borough',
                color='Commercial %',
                color_continuous_scale='Reds',
                text=[f'{x:.1f}%' for x in commercial_by_borough['Commercial %']]
            )
            fig_density.update_traces(textposition='outside')
            fig_density.update_layout(
                height=400,
                showlegend=False,
                xaxis_title='Borough',
                yaxis_title='Commercial Listing Rate (%)',
                yaxis=dict(tickformat='.1f')
            )
        else:
            host_size_violations = df[df['room_type'] == 'Entire home/apt'].groupby('host_size').size().reset_index()
            host_size_violations.columns = ['Host Size', 'Listings']
            
            fig_density = px.bar(
                host_size_violations,
                x='Host Size',
                y='Listings',
                title='🏬 Entire Home Listings by Host Portfolio Size',
                color='Listings',
                color_continuous_scale='Oranges'
            )
            fig_density.update_layout(
                height=400,
                xaxis_title='Host Portfolio Size',
                yaxis_title='Number of Listings',
                yaxis=dict(tickformat=',d')
            )
        self.commercial_density.set_figure(fig_density, is_dark)
        
        # Violations by Borough
        borough_violations = df_violations.groupby('neighbourhood_group').size().reset_index()
        borough_violations.columns = ['Borough', 'Violations']
        
        # Consistent borough color mapping
        borough_color_map = {
            'Manhattan': '#f59e0b',
            'Brooklyn': '#ef4444',
            'Queens': '#10b981',
            'Bronx': '#3b82f6',
            'Staten Island': '#8b5cf6'
        }
        
        fig_borough = px.pie(
            borough_violations,
            values='Violations',
            names='Borough',
            color='Borough',
            color_discrete_map=borough_color_map,
            title='🗺️ Potential Violations by Borough'
        )
        fig_borough.update_layout(height=400)
        fig_borough.update_traces(textposition='inside', textinfo='percent+label')
        self.borough_violations.set_figure(fig_borough, is_dark)
        
        # Availability Analysis
        fig_avail = go.Figure()
        
        for room_type in df['room_type'].unique():
            room_data = df[df['room_type'] == room_type]['availability_365']
            fig_avail.add_trace(go.Violin(
                y=room_data,
                name=room_type,
                box_visible=True,
                meanline_visible=True
            ))
        
        fig_avail.update_layout(
            title='📊 Availability Distribution by Room Type',
            xaxis_title='Room Type',
            yaxis_title='Availability (Days per Year)',
            height=400,
            showlegend=True,
            yaxis=dict(tickformat=',d')
        )
        fig_avail.add_hline(y=180, line_dash="dash", line_color="#f85149",
                          annotation_text="Housing Impact Threshold (180 days)", annotation_position="top right")
        self.availability_analysis.set_figure(fig_avail, is_dark)
        
        # Update Commercial vs Regular Comparison Table
        commercial_stats = self.data_manager.get_commercial_stats()
        
        if commercial_stats and 'commercial' in commercial_stats and 'regular' in commercial_stats:
            comm = commercial_stats['commercial']
            reg = commercial_stats['regular']
            
            # Calculate estimated revenue
            comm_revenue = comm.get('median_price', 0) * (365 - comm.get('median_availability', 0))
            reg_revenue = reg.get('median_price', 0) * (365 - reg.get('median_availability', 0))
            
            metrics = [
                ('Count', f"{comm.get('count', 0):,}", f"{reg.get('count', 0):,}", 
                 f"{comm.get('count', 0) / len(df) * 100:.1f}% commercial" if len(df) > 0 else "N/A"),
                ('Median Price', f"${comm.get('median_price', 0):.0f}", f"${reg.get('median_price', 0):.0f}",
                 f"+${comm.get('median_price', 0) - reg.get('median_price', 0):.0f}"),
                ('Median Reviews', f"{comm.get('median_reviews', 0):.0f}", f"{reg.get('median_reviews', 0):.0f}",
                 f"+{comm.get('median_reviews', 0) - reg.get('median_reviews', 0):.0f}"),
                ('Median Availability', f"{comm.get('median_availability', 0):.0f} days", f"{reg.get('median_availability', 0):.0f} days",
                 f"+{comm.get('median_availability', 0) - reg.get('median_availability', 0):.0f} days"),
                ('Est. Revenue/Year', f"${comm_revenue:,.0f}", f"${reg_revenue:,.0f}",
                 f"+${comm_revenue - reg_revenue:,.0f}"),
            ]
            
            self.comparison_table.setRowCount(len(metrics))
            for i, (metric, commercial, regular, diff) in enumerate(metrics):
                self.comparison_table.setItem(i, 0, QTableWidgetItem(metric))
                self.comparison_table.setItem(i, 1, QTableWidgetItem(commercial))
                self.comparison_table.setItem(i, 2, QTableWidgetItem(regular))
                self.comparison_table.setItem(i, 3, QTableWidgetItem(diff))
