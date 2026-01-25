"""
Data Manager - Handles data loading and processing for the dashboard
Enhanced with app_en.py features: commercial flagging, value scores, temporal data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from PySide6.QtCore import QObject, Signal, QThread


class DataLoader(QThread):
    """Background thread for loading data"""
    
    finished = Signal(object)
    progress = Signal(int)
    error = Signal(str)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            self.progress.emit(10)
            df = pd.read_csv(self.file_path)
            self.progress.emit(50)
            
            # Clean data
            df = self._clean_data(df)
            self.progress.emit(100)
            
            self.finished.emit(df)
        except Exception as e:
            self.error.emit(str(e))
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return DataManager.process_dataframe(df)


class DataManager(QObject):
    """Manages all data operations for the dashboard"""
    
    data_loaded = Signal()
    data_filtered = Signal()
    filters_resulted_empty = Signal()
    
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.filtered_df: Optional[pd.DataFrame] = None
        self._filters: Dict = {}
    
    @staticmethod
    def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Process and enhance dataframe with derived columns"""
        # Outlier filtering (price: 10-1000$, minimum_nights < 31)
        df = df[(df['price'] >= 10) & (df['price'] <= 1000)]
        df = df[df['minimum_nights'] < 31]
        df = df.dropna(subset=['latitude', 'longitude', 'price'])
        
        # Temporal data transformation
        df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
        df['review_month'] = df['last_review'].dt.to_period('M').astype(str)
        df['review_year'] = df['last_review'].dt.year
        
        # Commercial listing flagging (availability > 300 OR host_listings > 5)
        df['is_commercial'] = ((df['availability_365'] > 300) | 
                               (df['calculated_host_listings_count'] > 5))
        
        # Price category
        df['price_category'] = pd.cut(
            df['price'],
            bins=[0, 50, 100, 200, 500, 1000],
            labels=['Budget ($0-50)', 'Economy ($50-100)', 
                   'Mid-range ($100-200)', 'Upscale ($200-500)', 
                   'Luxury ($500+)']
        )
        
        # Host size category
        host_listing_counts = df['host_id'].value_counts()
        df['host_listing_count'] = df['host_id'].map(host_listing_counts)
        df['host_size'] = pd.cut(
            df['host_listing_count'],
            bins=[0, 1, 5, 10, float('inf')],
            labels=['Single (1)', 'Small (2-5)', 'Medium (6-10)', 'Mega (10+)']
        )
        
        # Host category (same as app_en.py)
        df['host_category'] = pd.cut(
            df['calculated_host_listings_count'],
            bins=[0, 1, 5, 10, float('inf')],
            labels=['Single (1)', 'Small (2-5)', 'Medium (6-10)', 'Mega (10+)']
        )
        
        # Value score (reviews / price) - for Traveler view
        df['value_score'] = (df['number_of_reviews'] / (df['price'] + 1)) * 100
        
        # Estimated annual revenue - for Investor view
        df['estimated_annual_revenue'] = df['price'] * df['availability_365'] * 0.7  # 70% occupancy
        
        return df
    
    def load_data(self, file_path: str):
        """Load data from CSV file"""
        self.loader = DataLoader(file_path)
        self.loader.finished.connect(self._on_data_loaded)
        self.loader.start()
    
    def load_data_sync(self, file_path: str):
        """Load data synchronously with optimizations"""
        # Use optimized CSV reading
        df = pd.read_csv(file_path, 
                        low_memory=True,  # Use chunks for large files
                        engine='c')  # Faster C engine
        df = self.process_dataframe(df)
        
        self.df = df
        self.filtered_df = df  # No copy needed initially, just reference
        self.data_loaded.emit()
    
    def _on_data_loaded(self, df: pd.DataFrame):
        self.df = df
        self.filtered_df = df  # Reference instead of copy
        self.data_loaded.emit()
    
    def apply_filters(self, filters: Dict):
        """Apply filters to the dataset"""
        self._filters = filters
        # Keep reference to previous for empty check (no copy needed)
        previous_filtered = self.filtered_df
        
        # Start with full dataset (use boolean indexing, no copy)
        mask = pd.Series([True] * len(self.df), index=self.df.index)
        
        # Neighbourhood group filter
        if 'neighbourhood_group' in filters and filters['neighbourhood_group']:
            mask &= self.df['neighbourhood_group'].isin(filters['neighbourhood_group'])
        
        # Neighbourhood detail filter
        if 'neighbourhood' in filters and filters['neighbourhood'] and filters['neighbourhood'] != 'all':
            mask &= self.df['neighbourhood'] == filters['neighbourhood']
        
        # Room type filter
        if 'room_type' in filters and filters['room_type']:
            mask &= self.df['room_type'].isin(filters['room_type'])
        
        # Apply mask to get filtered dataframe
        self.filtered_df = self.df[mask]
        
        # Price range filter
        if 'price_range' in filters:
            min_price, max_price = filters['price_range']
            mask &= (self.df['price'] >= min_price) & (self.df['price'] <= max_price)
        
        # Minimum nights filter
        if 'min_nights' in filters:
            mask &= self.df['minimum_nights'] <= filters['min_nights']
        
        # Minimum reviews filter
        if 'min_reviews' in filters and filters['min_reviews'] > 0:
            mask &= self.df['number_of_reviews'] >= filters['min_reviews']
        
        # Host category filter
        if 'host_category' in filters and filters['host_category'] and filters['host_category'] != 'all':
            mask &= self.df['host_category'] == filters['host_category']
        
        # Commercial listing filter
        if 'commercial_only' in filters and filters['commercial_only']:
            mask &= self.df['is_commercial'] == True
        
        # Apply mask to get filtered dataframe
        self.filtered_df = self.df[mask]
        
        # Check if filtering resulted in empty dataset
        if len(self.filtered_df) == 0:
            # Restore previous filtered data
            self.filtered_df = previous_filtered
            # Emit signal with empty result flag
            self.filters_resulted_empty.emit()
            return
        
        # Emit signal that filtering is complete
        self.data_filtered.emit()
    
    def get_stats(self) -> Dict:
        """Get summary statistics"""
        if self.filtered_df is None:
            return {}
        
        return {
            'total_listings': len(self.filtered_df),
            'avg_price': self.filtered_df['price'].mean(),
            'median_price': self.filtered_df['price'].median(),
            'total_hosts': self.filtered_df['host_id'].nunique(),
            'avg_reviews': self.filtered_df['number_of_reviews'].mean(),
            'total_reviews': self.filtered_df['number_of_reviews'].sum(),
            'commercial_count': self.filtered_df['is_commercial'].sum() if 'is_commercial' in self.filtered_df.columns else 0,
            'avg_availability': self.filtered_df['availability_365'].mean(),
        }
    
    def get_neighbourhood_stats(self) -> pd.DataFrame:
        """Get statistics by neighbourhood"""
        if self.filtered_df is None:
            return pd.DataFrame()
        
        return self.filtered_df.groupby('neighbourhood_group').agg({
            'id': 'count',
            'price': ['mean', 'median'],
            'number_of_reviews': 'sum',
            'availability_365': 'mean'
        }).round(2)
    
    def get_room_type_stats(self) -> pd.DataFrame:
        """Get statistics by room type"""
        if self.filtered_df is None:
            return pd.DataFrame()
        
        return self.filtered_df.groupby('room_type').agg({
            'id': 'count',
            'price': ['mean', 'median'],
            'number_of_reviews': 'mean'
        }).round(2)
    
    def get_price_distribution(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get price distribution data"""
        if self.filtered_df is None:
            return np.array([]), np.array([])
        
        prices = self.filtered_df['price'].values
        hist, bins = np.histogram(prices, bins=50)
        return hist, bins
    
    def get_top_hosts(self, n: int = 10) -> pd.DataFrame:
        """Get top hosts by listing count"""
        if self.filtered_df is None:
            return pd.DataFrame()
        
        host_stats = self.filtered_df.groupby('host_id').agg({
            'host_name': 'first',
            'id': 'count',
            'price': 'mean',
            'number_of_reviews': 'sum'
        }).reset_index()
        
        host_stats.columns = ['host_id', 'host_name', 'listing_count', 
                              'avg_price', 'total_reviews']
        
        return host_stats.nlargest(n, 'listing_count')
    
    def get_top_value_listings(self, n: int = 10) -> pd.DataFrame:
        """Get top value listings by value score (reviews/price)
        
        Filters for practical stays (<=7 nights minimum) and calculates
        normalized value score for better comparison.
        """
        if self.filtered_df is None:
            return pd.DataFrame()
        
        # Filter for practical travel stays (minimum_nights <= 7)
        df_value = self.filtered_df[self.filtered_df['minimum_nights'] <= 7].copy()
        
        if len(df_value) == 0:
            return pd.DataFrame()
        
        # Calculate normalized value score if not exists
        if 'value_score' not in df_value.columns or True:  # Always recalculate for consistency
            # Method 1: Simple reviews per dollar (better for travelers)
            df_value['value_score'] = df_value['number_of_reviews'] / (df_value['price'] + 1)
        
        return df_value.nlargest(n, 'value_score')[
            ['name', 'neighbourhood', 'price', 'number_of_reviews', 'room_type', 'value_score', 'minimum_nights']
        ]
    
    def get_commercial_stats(self) -> Dict:
        """Get commercial vs regular listing comparison"""
        if self.filtered_df is None or 'is_commercial' not in self.filtered_df.columns:
            return {}
        
        commercial = self.filtered_df[self.filtered_df['is_commercial'] == True]
        regular = self.filtered_df[self.filtered_df['is_commercial'] == False]
        
        return {
            'commercial': {
                'count': len(commercial),
                'median_price': commercial['price'].median() if len(commercial) > 0 else 0,
                'median_availability': commercial['availability_365'].median() if len(commercial) > 0 else 0,
                'median_reviews': commercial['number_of_reviews'].median() if len(commercial) > 0 else 0,
            },
            'regular': {
                'count': len(regular),
                'median_price': regular['price'].median() if len(regular) > 0 else 0,
                'median_availability': regular['availability_365'].median() if len(regular) > 0 else 0,
                'median_reviews': regular['number_of_reviews'].median() if len(regular) > 0 else 0,
            }
        }
    
    def get_roi_data(self, top_n: int = 10) -> pd.DataFrame:
        """Get ROI analysis data by segment"""
        if self.filtered_df is None:
            return pd.DataFrame()
        
        roi_data = self.filtered_df.groupby(['neighbourhood_group', 'room_type']).agg({
            'price': 'median',
            'availability_365': 'median',
            'number_of_reviews': 'median'
        }).reset_index()
        
        roi_data['estimated_annual_revenue'] = roi_data['price'] * roi_data['availability_365'] * 0.7
        roi_data = roi_data.sort_values('estimated_annual_revenue', ascending=False)
        
        return roi_data.head(top_n)
    
    def get_host_category_stats(self) -> pd.DataFrame:
        """Get listing distribution by host category"""
        if self.filtered_df is None or 'host_category' not in self.filtered_df.columns:
            return pd.DataFrame()
        
        return self.filtered_df.groupby('host_category').size().reset_index(name='count')
    
    def get_monthly_review_trend(self) -> pd.DataFrame:
        """Get monthly review activity trend"""
        if self.filtered_df is None or 'last_review' not in self.filtered_df.columns:
            return pd.DataFrame()
        
        temporal_df = self.filtered_df[self.filtered_df['last_review'].notna()].copy()
        if len(temporal_df) == 0:
            return pd.DataFrame()
        
        temporal_df['review_month'] = temporal_df['last_review'].dt.to_period('M')
        monthly_reviews = temporal_df.groupby('review_month').size().reset_index(name='count')
        monthly_reviews['review_month'] = monthly_reviews['review_month'].astype(str)
        
        return monthly_reviews
    
    def get_neighbourhoods_for_borough(self, borough: str) -> List[str]:
        """Get list of neighbourhoods for a specific borough"""
        if self.df is None:
            return []
        
        if borough == 'all' or borough == [] or borough is None:
            return sorted(self.df['neighbourhood'].unique().tolist())
        
        # Handle both single borough and list of boroughs
        if isinstance(borough, list):
            if len(borough) == 0:
                return sorted(self.df['neighbourhood'].unique().tolist())
            return sorted(self.df[self.df['neighbourhood_group'].isin(borough)]['neighbourhood'].unique().tolist())
        
        return sorted(self.df[self.df['neighbourhood_group'] == borough]['neighbourhood'].unique().tolist())
    
    def get_map_data(self, sample_size: int = 5000) -> pd.DataFrame:
        """Get data for map visualization"""
        if self.filtered_df is None:
            return pd.DataFrame()
        
        if len(self.filtered_df) > sample_size:
            return self.filtered_df.sample(n=sample_size, random_state=42)
        return self.filtered_df
    
    def export_to_csv(self, file_path: str):
        """Export filtered data to CSV"""
        if self.filtered_df is not None:
            export_cols = ['name', 'neighbourhood_group', 'neighbourhood', 'room_type', 
                          'price', 'number_of_reviews', 'availability_365', 'host_category']
            export_cols = [c for c in export_cols if c in self.filtered_df.columns]
            self.filtered_df[export_cols].to_csv(file_path, index=False)
    
    def get_unique_values(self, column: str) -> List:
        """Get unique values for a column"""
        if self.df is None:
            return []
        return self.df[column].unique().tolist()
    
    def get_neighbourhoods(self) -> List[str]:
        """Get list of neighbourhood groups"""
        return self.get_unique_values('neighbourhood_group')
    
    def get_room_types(self) -> List[str]:
        """Get list of room types"""
        return self.get_unique_values('room_type')
    
    def get_host_categories(self) -> List[str]:
        """Get list of host categories"""
        return ['all', 'Single (1)', 'Small (2-5)', 'Medium (6-10)', 'Mega (10+)']
    
    def get_missing_data_stats(self) -> Dict:
        """Get statistics about missing data in the dataset"""
        if self.filtered_df is None:
            return {}
        
        total_rows = len(self.filtered_df)
        missing_stats = {}
        
        # Check key columns for missing data
        key_columns = ['name', 'host_name', 'last_review', 'reviews_per_month']
        
        for col in key_columns:
            if col in self.filtered_df.columns:
                missing_count = self.filtered_df[col].isnull().sum()
                if missing_count > 0:
                    missing_stats[col] = {
                        'count': int(missing_count),
                        'percentage': round((missing_count / total_rows) * 100, 1)
                    }
        
        return missing_stats
    
    def get_data_quality_score(self) -> Dict:
        """Calculate data quality metrics"""
        if self.filtered_df is None:
            return {'score': 0, 'details': {}}
        
        total_rows = len(self.filtered_df)
        total_cells = total_rows * len(self.filtered_df.columns)
        missing_cells = self.filtered_df.isnull().sum().sum()
        
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        # Check for outliers (already filtered, so should be minimal)
        price_outliers = ((self.filtered_df['price'] < 10) | 
                         (self.filtered_df['price'] > 1000)).sum()
        
        return {
            'score': round(completeness, 1),
            'total_records': total_rows,
            'missing_cells': int(missing_cells),
            'completeness': round(completeness, 1),
            'outliers_filtered': int(price_outliers)
        }
    
    def get_uncertainty_indicators(self) -> Dict:
        """Get uncertainty indicators for predictions and estimates"""
        if self.filtered_df is None:
            return {}
        
        # Calculate confidence intervals for key metrics
        import numpy as np
        
        # Price statistics with confidence intervals
        prices = self.filtered_df['price'].values
        price_mean = np.mean(prices)
        price_std = np.std(prices)
        price_ci_95 = 1.96 * (price_std / np.sqrt(len(prices)))
        
        # Revenue estimates with uncertainty
        if 'estimated_annual_revenue' in self.filtered_df.columns:
            revenues = self.filtered_df['estimated_annual_revenue'].values
            revenue_mean = np.mean(revenues)
            revenue_std = np.std(revenues)
            revenue_ci_95 = 1.96 * (revenue_std / np.sqrt(len(revenues)))
        else:
            revenue_mean = 0
            revenue_ci_95 = 0
        
        return {
            'price': {
                'mean': round(price_mean, 2),
                'ci_lower': round(price_mean - price_ci_95, 2),
                'ci_upper': round(price_mean + price_ci_95, 2),
                'margin_of_error': round(price_ci_95, 2)
            },
            'revenue': {
                'mean': round(revenue_mean, 2),
                'ci_lower': round(revenue_mean - revenue_ci_95, 2),
                'ci_upper': round(revenue_mean + revenue_ci_95, 2),
                'margin_of_error': round(revenue_ci_95, 2)
            },
            'note': '95% confidence interval'
        }
