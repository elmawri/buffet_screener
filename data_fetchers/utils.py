"""
Utility functions for Buffett Screener
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

def safe_divide(numerator, denominator, default=None):
    """Safely divide two numbers, returning default if denominator is 0 or None"""
    try:
        if denominator is None or denominator == 0 or pd.isna(denominator):
            return default
        if numerator is None or pd.isna(numerator):
            return default
        return numerator / denominator
    except:
        return default

def calculate_cagr(start_value, end_value, periods):
    """Calculate Compound Annual Growth Rate"""
    try:
        if start_value is None or end_value is None or start_value <= 0:
            return None
        if periods <= 0:
            return None
        return (((end_value / start_value) ** (1 / periods)) - 1) * 100
    except:
        return None

def calculate_std_dev(values):
    """Calculate standard deviation, handling None values"""
    try:
        clean_values = [v for v in values if v is not None and not pd.isna(v)]
        if len(clean_values) < 2:
            return None
        return np.std(clean_values)
    except:
        return None

def count_down_years(values):
    """Count number of years with negative growth"""
    try:
        count = 0
        for i in range(1, len(values)):
            if values[i] is not None and values[i-1] is not None:
                if values[i] < values[i-1]:
                    count += 1
        return count
    except:
        return None

def get_last_updated():
    """Return current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def cache_data(cache_key, data, cache_dir=".cache"):
    """Cache data to avoid repeated API calls"""
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    with open(cache_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f)

def load_cached_data(cache_key, max_age_days=1, cache_dir=".cache"):
    """Load cached data if available and not expired"""
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
        
        cache_time = datetime.fromisoformat(cached['timestamp'])
        age_days = (datetime.now() - cache_time).days
        
        if age_days <= max_age_days:
            return cached['data']
    except:
        pass
    
    return None

def format_currency(value):
    """Format value as currency string"""
    if value is None or pd.isna(value):
        return ""
    return f"${value:,.0f}"

def format_percentage(value):
    """Format value as percentage string"""
    if value is None or pd.isna(value):
        return ""
    return f"{value:.2f}%"
