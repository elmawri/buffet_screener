"""
Yahoo Finance data fetcher for Buffett Screener
"""
import yfinance as yf
import pandas as pd
from data_fetchers.utils import (
    safe_divide, calculate_cagr, calculate_std_dev, 
    count_down_years, load_cached_data, cache_data
)

class YahooFinanceFetcher:
    def __init__(self, ticker, use_cache=True):
        self.ticker = ticker
        self.use_cache = use_cache
        self.stock = None
        self._load_stock()
    
    def _load_stock(self):
        """Load stock data from Yahoo Finance or cache"""
        cache_key = f"yf_{self.ticker}"
        
        if self.use_cache:
            cached = load_cached_data(cache_key)
            if cached:
                # For cached data, we still need to create yf.Ticker for some methods
                self.stock = yf.Ticker(self.ticker)
                return
        
        self.stock = yf.Ticker(self.ticker)
    
    def get_info(self):
        """Get company info dict"""
        try:
            return self.stock.info
        except:
            return {}
    
    def get_basic_info(self):
        """Get basic company information for Tickers sheet"""
        info = self.get_info()
        return {
            'ticker': self.ticker,
            'company': info.get('longName', ''),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'country': info.get('country', ''),
            'currency': info.get('currency', ''),
            'exchange': info.get('exchange', ''),
            'cik': info.get('cik', ''),
            'isin': info.get('isin', '')
        }
    
    def get_financials(self, statement_type='income', annual=True):
        """Get financial statements
        
        Args:
            statement_type: 'income', 'balance', or 'cashflow'
            annual: True for annual, False for quarterly
        """
        try:
            if statement_type == 'income':
                df = self.stock.financials if annual else self.stock.quarterly_financials
            elif statement_type == 'balance':
                df = self.stock.balance_sheet if annual else self.stock.quarterly_balance_sheet
            elif statement_type == 'cashflow':
                df = self.stock.cashflow if annual else self.stock.quarterly_cashflow
            else:
                return pd.DataFrame()
            
            return df
        except:
            return pd.DataFrame()
    
    def get_historical_data(self, period="10y"):
        """Get historical price data"""
        try:
            hist = self.stock.history(period=period)
            return hist
        except:
            return pd.DataFrame()
    
    def get_roe_roic_data(self):
        """Get ROE and ROIC metrics"""
        info = self.get_info()
        
        try:
            # Get ROE
            roe_ttm = info.get('returnOnEquity', None)
            if roe_ttm:
                roe_ttm = roe_ttm * 100  # Convert to percentage
            
            # Get historical financials for 5Y average
            income = self.get_financials('income', annual=True)
            balance = self.get_financials('balance', annual=True)
            
            # Calculate 5Y avg ROE
            roe_values = []
            if not income.empty and not balance.empty:
                for col in income.columns[:5]:  # Last 5 years
                    net_income = income.loc['Net Income', col] if 'Net Income' in income.index else None
                    equity = balance.loc['Stockholders Equity', col] if 'Stockholders Equity' in balance.index else None
                    
                    roe = safe_divide(net_income, equity)
                    if roe:
                        roe_values.append(roe * 100)
            
            roe_5y_avg = sum(roe_values) / len(roe_values) if roe_values else None
            
            # Calculate ROIC (simplified: NOPAT / Invested Capital)
            roic_ttm = None
            roic_5y_avg = None
            
            # Get FCF margin
            cashflow = self.get_financials('cashflow', annual=True)
            fcf_values = []
            
            if not cashflow.empty and not income.empty:
                for col in cashflow.columns[:5]:
                    fcf = cashflow.loc['Free Cash Flow', col] if 'Free Cash Flow' in cashflow.index else None
                    revenue = income.loc['Total Revenue', col] if 'Total Revenue' in income.index else None
                    
                    fcf_margin = safe_divide(fcf, revenue)
                    if fcf_margin:
                        fcf_values.append(fcf_margin * 100)
            
            fcf_margin_5y = sum(fcf_values) / len(fcf_values) if fcf_values else None
            
            # Get CapEx/Sales
            capex_values = []
            if not cashflow.empty and not income.empty:
                for col in cashflow.columns[:5]:
                    capex = cashflow.loc['Capital Expenditure', col] if 'Capital Expenditure' in cashflow.index else None
                    revenue = income.loc['Total Revenue', col] if 'Total Revenue' in income.index else None
                    
                    if capex and revenue:
                        capex_ratio = abs(capex) / revenue  # CapEx is negative
                        capex_values.append(capex_ratio * 100)
            
            capex_sales_5y = sum(capex_values) / len(capex_values) if capex_values else None
            
            return {
                'roe_ttm': roe_ttm,
                'roe_5y_avg': roe_5y_avg,
                'roic_ttm': roic_ttm,
                'roic_5y_avg': roic_5y_avg,
                'fcf_margin_5y_avg': fcf_margin_5y,
                'capex_sales_5y_avg': capex_sales_5y
            }
        except Exception as e:
            print(f"Error getting ROE/ROIC for {self.ticker}: {e}")
            return {}
    
    def get_operating_history_data(self):
        """Get operating history metrics"""
        try:
            info = self.get_info()
            income = self.get_financials('income', annual=True)
            
            # Get historical data for 10 years
            if income.empty:
                return {}
            
            # Extract revenue and EPS for last 10 years
            revenues = []
            eps_values = []
            years_count = min(10, len(income.columns))
            
            for col in income.columns[:years_count]:
                rev = income.loc['Total Revenue', col] if 'Total Revenue' in income.index else None
                if rev:
                    revenues.append(rev)
                
                # EPS from info or calculate
                net_income = income.loc['Net Income', col] if 'Net Income' in income.index else None
                shares = income.loc['Basic Average Shares', col] if 'Basic Average Shares' in income.index else None
                eps = safe_divide(net_income, shares) if net_income and shares else None
                if eps:
                    eps_values.append(eps)
            
            # Calculate metrics
            rev_cagr = calculate_cagr(revenues[-1], revenues[0], len(revenues)-1) if len(revenues) >= 2 else None
            eps_cagr = calculate_cagr(eps_values[-1], eps_values[0], len(eps_values)-1) if len(eps_values) >= 2 else None
            
            rev_down_years = count_down_years(list(reversed(revenues)))
            eps_down_years = count_down_years(list(reversed(eps_values)))
            
            years_profitable = sum(1 for eps in eps_values if eps and eps > 0)
            
            return {
                'ipo_year': '',  # Not available from yfinance
                'years_since_ipo': '',
                'years_profitable': years_profitable,
                'rev_10y_cagr': rev_cagr,
                'eps_10y_cagr': eps_cagr,
                'rev_down_years': rev_down_years,
                'eps_down_years': eps_down_years
            }
        except Exception as e:
            print(f"Error getting operating history for {self.ticker}: {e}")
            return {}
    
    def get_leverage_data(self):
        """Get leverage metrics"""
        try:
            info = self.get_info()
            balance = self.get_financials('balance', annual=True)
            income = self.get_financials('income', annual=True)
            
            # Current metrics
            debt_equity_ttm = info.get('debtToEquity', None)
            if debt_equity_ttm:
                debt_equity_ttm = debt_equity_ttm / 100  # Yahoo returns as percentage
            
            # 5Y average debt/equity
            debt_equity_values = []
            if not balance.empty:
                for col in balance.columns[:5]:
                    total_debt = balance.loc['Total Debt', col] if 'Total Debt' in balance.index else None
                    equity = balance.loc['Stockholders Equity', col] if 'Stockholders Equity' in balance.index else None
                    
                    de = safe_divide(total_debt, equity)
                    if de:
                        debt_equity_values.append(de)
            
            debt_equity_5y = sum(debt_equity_values) / len(debt_equity_values) if debt_equity_values else None
            
            # Interest coverage (EBIT / Interest Expense)
            interest_coverage = None
            if not income.empty:
                latest = income.columns[0]
                ebit = income.loc['EBIT', latest] if 'EBIT' in income.index else None
                interest = income.loc['Interest Expense', latest] if 'Interest Expense' in income.index else None
                interest_coverage = safe_divide(ebit, abs(interest)) if ebit and interest else None
            
            # Cash and debt
            cash = balance.iloc[:, 0].get('Cash And Cash Equivalents', None) if not balance.empty else None
            total_debt = balance.iloc[:, 0].get('Total Debt', None) if not balance.empty else None
            
            return {
                'debt_equity_ttm': debt_equity_ttm,
                'debt_equity_5y': debt_equity_5y,
                'interest_coverage': interest_coverage,
                'cash': cash,
                'total_debt': total_debt
            }
        except Exception as e:
            print(f"Error getting leverage for {self.ticker}: {e}")
            return {}
    
    def get_valuation_data(self):
        """Get valuation metrics for Price Value sheet"""
        try:
            info = self.get_info()
            
            data = {
                'pe_ttm': info.get('trailingPE', None),
                'pb_mrq': info.get('priceToBook', None),
                'ev_ebit_ttm': info.get('enterpriseToEbitda', None),  # Close enough
                'market_cap': info.get('marketCap', None),
                'enterprise_value': info.get('enterpriseValue', None)
            }
            
            # Get historical for medians (would need more complex logic)
            # For now, just return current values
            
            return data
        except Exception as e:
            print(f"Error getting valuation for {self.ticker}: {e}")
            return {}
