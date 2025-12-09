"""
Third-party data sources (FRED, etc.)
"""
import requests

class FREDFetcher:
    """Fetch data from FRED (Federal Reserve Economic Data)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def get_10y_treasury_yield(self):
        """Get current 10-year Treasury yield"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': 'DGS10',  # 10-Year Treasury Constant Maturity Rate
                'api_key': self.api_key,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': 1
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'observations' in data and len(data['observations']) > 0:
                return float(data['observations'][0]['value'])
        except Exception as e:
            print(f"FRED API error: {e}")
        
        return None
