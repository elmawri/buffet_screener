"""
Financial Modeling Prep (FMP) Data Fetcher - Complete Implementation
Fetches historical financials, ratios, and pre-calculated metrics
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime
import statistics

class FMPFetcher:
    """Fetch data from Financial Modeling Prep API"""
    
    def __init__(self, api_key: str):
        """
        Initialize FMP fetcher
        Args:
            api_key: FMP API key
        """
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.base_url_v4 = "https://financialmodelingprep.com/api/v4"
    
    def _get(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request"""
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"FMP API error on {endpoint}: {e}")
            return None
    
    def _get_v4(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request to v4 endpoints"""
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url_v4}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"FMP API v4 error on {endpoint}: {e}")
            return None
    
    def get_company_profile(self, ticker: str) -> Optional[Dict]:
        """Get company profile with basic info"""
        data = self._get(f"profile/{ticker}")
        if data and isinstance(data, list) and len(data) > 0:
            return data[0]
        return None
    
    def get_historical_financials(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """
        Get historical income statements
        Args:
            ticker: Stock ticker
            period: 'annual' or 'quarter'
            limit: Number of periods to fetch
        """
        return self._get(f"income-statement/{ticker}", {'period': period, 'limit': limit})
    
    def get_balance_sheet(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """Get historical balance sheets"""
        return self._get(f"balance-sheet-statement/{ticker}", {'period': period, 'limit': limit})
    
    def get_cash_flow(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """Get historical cash flow statements"""
        return self._get(f"cash-flow-statement/{ticker}", {'period': period, 'limit': limit})
    
    def get_key_metrics(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """
        Get pre-calculated key metrics (ROE, ROIC, margins, etc.)
        This is gold - saves us from calculating everything
        """
        return self._get(f"key-metrics/{ticker}", {'period': period, 'limit': limit})
    
    def get_financial_ratios(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """Get pre-calculated financial ratios"""
        return self._get(f"ratios/{ticker}", {'period': period, 'limit': limit})
    
    def get_enterprise_values(self, ticker: str, period: str = "annual", limit: int = 10) -> Optional[List[Dict]]:
        """Get historical enterprise values and EV/EBITDA"""
        return self._get(f"enterprise-values/{ticker}", {'period': period, 'limit': limit})
    
    def get_historical_price(self, ticker: str, from_date: str, to_date: str) -> Optional[List[Dict]]:
        """Get historical stock prices"""
        return self._get(f"historical-price-full/{ticker}", {'from': from_date, 'to': to_date})
    
    def get_shares_float(self, ticker: str) -> Optional[Dict]:
        """Get shares outstanding and float"""
        return self._get(f"shares_float", {'symbol': ticker})
    
    def calculate_10y_metrics(self, ticker: str) -> Dict:
        """
        Calculate 10-year averages and medians for key metrics
        This is the main workhorse method
        """
        print(f"Calculating 10Y metrics for {ticker}...")
        
        metrics = {
            'ticker': ticker,
            'fetched_at': datetime.now().isoformat(),
            'roe': {},
            'roic': {},
            'margins': {},
            'valuation': {},
            'growth': {},
            'volatility': {}
        }
        
        # Get 10 years of data
        key_metrics = self.get_key_metrics(ticker, limit=10)
        ratios = self.get_financial_ratios(ticker, limit=10)
        financials = self.get_historical_financials(ticker, limit=10)
        enterprise = self.get_enterprise_values(ticker, limit=10)
        
        if key_metrics:
            # ROE 5Y and 10Y averages
            roe_values = [m['roe'] for m in key_metrics if m.get('roe') and m['roe'] != 0]
            if roe_values:
                metrics['roe']['avg_10y'] = statistics.mean(roe_values) * 100
                metrics['roe']['median_10y'] = statistics.median(roe_values) * 100
                metrics['roe']['avg_5y'] = statistics.mean(roe_values[:5]) * 100 if len(roe_values) >= 5 else None
                metrics['roe']['std_10y'] = statistics.stdev(roe_values) * 100 if len(roe_values) > 1 else 0
                print(f"  ROE 10Y Avg: {metrics['roe']['avg_10y']:.1f}%")
            
            # ROIC
            roic_values = [m['roic'] for m in key_metrics if m.get('roic') and m['roic'] != 0]
            if roic_values:
                metrics['roic']['avg_10y'] = statistics.mean(roic_values) * 100
                metrics['roic']['median_10y'] = statistics.median(roic_values) * 100
                metrics['roic']['avg_5y'] = statistics.mean(roic_values[:5]) * 100 if len(roic_values) >= 5 else None
                metrics['roic']['std_10y'] = statistics.stdev(roic_values) * 100 if len(roic_values) > 1 else 0
                print(f"  ROIC 10Y Avg: {metrics['roic']['avg_10y']:.1f}%")
            
            # FCF Margin
            fcf_margins = [m['freeCashFlowPerShare'] / m['revenuePerShare'] * 100 
                          for m in key_metrics 
                          if m.get('freeCashFlowPerShare') and m.get('revenuePerShare') 
                          and m['revenuePerShare'] != 0]
            if fcf_margins:
                metrics['margins']['fcf_avg_5y'] = statistics.mean(fcf_margins[:5]) if len(fcf_margins) >= 5 else None
        
        if ratios:
            # P/E Ratio - 10Y Median
            pe_values = [r['priceEarningsRatio'] for r in ratios if r.get('priceEarningsRatio') and r['priceEarningsRatio'] > 0]
            if pe_values:
                metrics['valuation']['pe_median_10y'] = statistics.median(pe_values)
                metrics['valuation']['pe_avg_10y'] = statistics.mean(pe_values)
                print(f"  P/E 10Y Median: {metrics['valuation']['pe_median_10y']:.1f}")
            
            # P/B Ratio - 10Y Median
            pb_values = [r['priceToBookRatio'] for r in ratios if r.get('priceToBookRatio') and r['priceToBookRatio'] > 0]
            if pb_values:
                metrics['valuation']['pb_median_10y'] = statistics.median(pb_values)
                metrics['valuation']['pb_avg_10y'] = statistics.mean(pb_values)
                print(f"  P/B 10Y Median: {metrics['valuation']['pb_median_10y']:.1f}")
            
            # Debt/Equity
            de_values = [r['debtEquityRatio'] for r in ratios if r.get('debtEquityRatio')]
            if de_values:
                metrics['leverage'] = {
                    'debt_equity_avg_5y': statistics.mean(de_values[:5]) if len(de_values) >= 5 else None
                }
        
        if enterprise:
            # EV/EBIT - 10Y Median
            ev_ebit_values = [e['enterpriseValueOverEBIT'] for e in enterprise 
                             if e.get('enterpriseValueOverEBIT') and e['enterpriseValueOverEBIT'] > 0]
            if ev_ebit_values:
                metrics['valuation']['ev_ebit_median_10y'] = statistics.median(ev_ebit_values)
                print(f"  EV/EBIT 10Y Median: {metrics['valuation']['ev_ebit_median_10y']:.1f}")
        
        if financials:
            # Revenue Growth (10Y CAGR)
            revenues = [f['revenue'] for f in financials if f.get('revenue')]
            if len(revenues) >= 2:
                years = len(revenues) - 1
                cagr = ((revenues[0] / revenues[-1]) ** (1 / years) - 1) * 100
                metrics['growth']['revenue_cagr_10y'] = cagr
                print(f"  Revenue CAGR 10Y: {cagr:.1f}%")
            
            # EPS Growth (10Y CAGR)
            eps_values = [f['eps'] for f in financials if f.get('eps')]
            if len(eps_values) >= 2 and eps_values[-1] > 0:
                years = len(eps_values) - 1
                eps_cagr = ((eps_values[0] / eps_values[-1]) ** (1 / years) - 1) * 100
                metrics['growth']['eps_cagr_10y'] = eps_cagr
                print(f"  EPS CAGR 10Y: {eps_cagr:.1f}%")
            
            # Revenue Volatility
            if len(revenues) > 1:
                rev_growth = [(revenues[i] / revenues[i+1] - 1) * 100 for i in range(len(revenues)-1)]
                metrics['volatility']['revenue_std'] = statistics.stdev(rev_growth) if len(rev_growth) > 1 else 0
                metrics['volatility']['revenue_cov'] = (metrics['volatility']['revenue_std'] / abs(statistics.mean(rev_growth))) if statistics.mean(rev_growth) != 0 else 0
            
            # Gross Margins
            gross_margins = [f['grossProfitRatio'] * 100 for f in financials if f.get('grossProfitRatio')]
            if gross_margins:
                metrics['margins']['gross_avg_5y'] = statistics.mean(gross_margins[:5]) if len(gross_margins) >= 5 else None
                metrics['margins']['gross_std_10y'] = statistics.stdev(gross_margins) if len(gross_margins) > 1 else 0
            
            # Operating Margins
            op_margins = [f['operatingIncomeRatio'] * 100 for f in financials if f.get('operatingIncomeRatio')]
            if op_margins:
                metrics['margins']['operating_avg_5y'] = statistics.mean(op_margins[:5]) if len(op_margins) >= 5 else None
                metrics['margins']['operating_std_10y'] = statistics.stdev(op_margins) if len(op_margins) > 1 else 0
        
        return metrics
    
    def get_crisis_performance(self, ticker: str) -> Dict:
        """
        Get actual financial performance during crisis periods
        2008-09 GFC and 2020 COVID
        """
        print(f"Fetching crisis performance for {ticker}...")
        
        crisis_data = {
            '2008_2009': {},
            '2020': {}
        }
        
        # Get historical financials
        financials = self.get_historical_financials(ticker, limit=20)  # Get more history
        
        if financials:
            # Find 2008-2009 data
            data_2007 = next((f for f in financials if '2007' in f.get('date', '')), None)
            data_2009 = next((f for f in financials if '2009' in f.get('date', '')), None)
            
            if data_2007 and data_2009:
                rev_change = ((data_2009['revenue'] - data_2007['revenue']) / data_2007['revenue']) * 100
                eps_change = ((data_2009['eps'] - data_2007['eps']) / data_2007['eps']) * 100 if data_2007['eps'] != 0 else None
                
                crisis_data['2008_2009'] = {
                    'revenue_change_pct': rev_change,
                    'eps_change_pct': eps_change
                }
                print(f"  2008-09: Revenue {rev_change:+.1f}%, EPS {eps_change:+.1f}%")
            
            # Find 2020 data
            data_2019 = next((f for f in financials if '2019' in f.get('date', '')), None)
            data_2020 = next((f for f in financials if '2020' in f.get('date', '')), None)
            
            if data_2019 and data_2020:
                rev_change = ((data_2020['revenue'] - data_2019['revenue']) / data_2019['revenue']) * 100
                eps_change = ((data_2020['eps'] - data_2019['eps']) / data_2019['eps']) * 100 if data_2019['eps'] != 0 else None
                
                crisis_data['2020'] = {
                    'revenue_change_pct': rev_change,
                    'eps_change_pct': eps_change
                }
                print(f"  2020: Revenue {rev_change:+.1f}%, EPS {eps_change:+.1f}%")
        
        return crisis_data
    
    def get_shares_outstanding_change(self, ticker: str) -> Dict:
        """Calculate 5Y change in shares outstanding (dilution/buybacks)"""
        print(f"Calculating shares outstanding change for {ticker}...")
        
        balance_sheets = self.get_balance_sheet(ticker, limit=6)
        
        if balance_sheets and len(balance_sheets) >= 2:
            current_shares = balance_sheets[0].get('commonStock', 0)
            five_years_ago_shares = balance_sheets[5].get('commonStock', 0) if len(balance_sheets) >= 6 else balance_sheets[-1].get('commonStock', 0)
            
            if current_shares and five_years_ago_shares:
                change_pct = ((current_shares - five_years_ago_shares) / five_years_ago_shares) * 100
                print(f"  Shares 5Y Change: {change_pct:+.1f}%")
                return {
                    'shares_5y_change_pct': change_pct,
                    'current_shares': current_shares,
                    'five_years_ago_shares': five_years_ago_shares
                }
        
        return {}
    
    def get_comprehensive_data(self, ticker: str) -> Dict:
        """
        Get all FMP data for a ticker
        This is the main method to call
        """
        print(f"\nFetching FMP data for {ticker}...")
        print("="*60)
        
        data = {
            'ticker': ticker,
            'fetched_at': datetime.now().isoformat(),
            'profile': None,
            'metrics_10y': None,
            'crisis_performance': None,
            'shares_change': None
        }
        
        # Company profile (includes IPO date, etc.)
        profile = self.get_company_profile(ticker)
        if profile:
            data['profile'] = {
                'ipo_date': profile.get('ipoDate'),
                'industry': profile.get('industry'),
                'sector': profile.get('sector'),
                'ceo': profile.get('ceo'),
                'description': profile.get('description')
            }
            if profile.get('ipoDate'):
                print(f"  IPO Date: {profile['ipoDate']}")
        
        # 10Y metrics (the gold mine)
        metrics = self.calculate_10y_metrics(ticker)
        data['metrics_10y'] = metrics
        
        # Crisis performance
        crisis = self.get_crisis_performance(ticker)
        data['crisis_performance'] = crisis
        
        # Shares change
        shares = self.get_shares_outstanding_change(ticker)
        data['shares_change'] = shares
        
        print("="*60)
        return data

# Example usage
if __name__ == "__main__":
    # Test with API key (would come from config)
    api_key = "YOUR_API_KEY_HERE"
    fetcher = FMPFetcher(api_key)
    
    # Test with a ticker
    data = fetcher.get_comprehensive_data("AAPL")
    
    import json
    print("\n" + "="*80)
    print("COMPREHENSIVE DATA:")
    print("="*80)
    print(json.dumps(data, indent=2))
