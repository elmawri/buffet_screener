"""
Historical Data Utilities
Extract and calculate 5Y averages, volatility, crisis performance
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class HistoricalDataExtractor:
    """Extract historical financial data for scoring"""
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
    
    def get_5y_financials(self):
        """Get 5-year financial metrics"""
        try:
            # Get financial statements
            income_stmt = self.stock.financials
            balance_sheet = self.stock.balance_sheet
            cash_flow = self.stock.cashflow
            
            # Get annual data (last 5 years)
            if income_stmt.empty:
                return {}
            
            # Reverse to chronological order
            income_stmt = income_stmt.iloc[:, :5]  # Last 5 years
            balance_sheet = balance_sheet.iloc[:, :5]
            cash_flow = cash_flow.iloc[:, :5]
            
            return {
                'income_statement': income_stmt,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
        except:
            return {}
    
    def calculate_roe_roic_metrics(self):
        """Calculate ROE and ROIC with 5Y averages"""
        try:
            financials = self.get_5y_financials()
            if not financials:
                return {}
            
            income = financials['income_statement']
            balance = financials['balance_sheet']
            
            # ROE = Net Income / Shareholders' Equity
            net_income = income.loc['Net Income'] if 'Net Income' in income.index else None
            equity = balance.loc['Stockholders Equity'] if 'Stockholders Equity' in balance.index else None
            
            roe_values = []
            if net_income is not None and equity is not None:
                for col in income.columns:
                    if col in balance.columns:
                        ni = net_income[col]
                        eq = equity[col]
                        if eq and eq != 0:
                            roe = (ni / eq) * 100
                            roe_values.append(roe)
            
            # ROIC = NOPAT / Invested Capital
            # Simplified: Operating Income * (1 - Tax Rate) / (Equity + Debt)
            roic_values = []
            # (Simplified calculation - full ROIC needs more detail)
            
            return {
                'roe_values': roe_values,
                'roe_avg': np.mean(roe_values) if roe_values else 0,
                'roe_std': np.std(roe_values) if roe_values else 0,
                'roic_values': roic_values,
                'roic_avg': np.mean(roic_values) if roic_values else 0,
                'roic_std': np.std(roic_values) if roic_values else 0
            }
        except Exception as e:
            print(f"Error calculating ROE/ROIC: {e}")
            return {}
    
    def calculate_revenue_earnings_volatility(self):
        """Calculate revenue and earnings volatility (CoV)"""
        try:
            financials = self.get_5y_financials()
            if not financials:
                return {}
            
            income = financials['income_statement']
            
            # Revenue volatility
            revenue_row = None
            for key in ['Total Revenue', 'Revenue', 'Total Revenues']:
                if key in income.index:
                    revenue_row = income.loc[key]
                    break
            
            revenue_values = list(revenue_row.values) if revenue_row is not None else []
            revenue_values = [v for v in revenue_values if v and not pd.isna(v)]
            
            # Earnings volatility
            earnings_row = None
            for key in ['Net Income', 'Net Income Common Stockholders']:
                if key in income.index:
                    earnings_row = income.loc[key]
                    break
            
            earnings_values = list(earnings_row.values) if earnings_row is not None else []
            earnings_values = [v for v in earnings_values if v and not pd.isna(v)]
            
            # Calculate CoV (Coefficient of Variation)
            def calc_cov(values):
                if len(values) < 2:
                    return 0
                mean = np.mean(values)
                std = np.std(values)
                return (std / mean * 100) if mean != 0 else 0
            
            return {
                'revenue_cov': calc_cov(revenue_values),
                'earnings_cov': calc_cov(earnings_values),
                'revenue_values': revenue_values,
                'earnings_values': earnings_values
            }
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return {}
    
    def get_crisis_performance(self):
        """Get performance during 2008-09 and 2020"""
        try:
            # Get historical prices and fundamentals
            hist = self.stock.history(start='2007-01-01', end='2021-12-31')
            
            if hist.empty:
                return {}
            
            # Try to get revenue data for these periods
            # This is tricky - we need annual reports
            # For now, we'll use stock price as proxy
            
            # 2008-09 Crisis
            try:
                price_2007 = hist['2007']['Close'].mean()
                price_2009 = hist['2009']['Close'].mean()
                price_change_2008 = ((price_2009 - price_2007) / price_2007 * 100) if price_2007 else 0
            except:
                price_change_2008 = 0
            
            # 2020 COVID
            try:
                price_2019 = hist['2019']['Close'].mean()
                price_2020 = hist['2020']['Close'].mean()
                price_change_2020 = ((price_2020 - price_2019) / price_2019 * 100) if price_2019 else 0
            except:
                price_change_2020 = 0
            
            return {
                'price_change_2008': price_change_2008,
                'price_change_2020': price_change_2020
                # Note: Ideally we'd get actual revenue/earnings data for these periods
            }
        except Exception as e:
            print(f"Error getting crisis performance: {e}")
            return {}
    
    def get_margin_metrics(self):
        """Calculate gross and operating margin averages"""
        try:
            financials = self.get_5y_financials()
            if not financials:
                return {}
            
            income = financials['income_statement']
            
            gross_margins = []
            operating_margins = []
            
            # Get revenue
            revenue_row = None
            for key in ['Total Revenue', 'Revenue']:
                if key in income.index:
                    revenue_row = income.loc[key]
                    break
            
            if revenue_row is None:
                return {}
            
            # Gross margin
            if 'Gross Profit' in income.index:
                gross_profit = income.loc['Gross Profit']
                for col in income.columns:
                    rev = revenue_row[col]
                    gp = gross_profit[col]
                    if rev and gp and rev != 0:
                        gross_margins.append((gp / rev) * 100)
            
            # Operating margin
            if 'Operating Income' in income.index:
                op_income = income.loc['Operating Income']
                for col in income.columns:
                    rev = revenue_row[col]
                    oi = op_income[col]
                    if rev and oi and rev != 0:
                        operating_margins.append((oi / rev) * 100)
            
            return {
                'gross_margin_avg': np.mean(gross_margins) if gross_margins else 0,
                'gross_margin_std': np.std(gross_margins) if gross_margins else 0,
                'operating_margin_avg': np.mean(operating_margins) if operating_margins else 0,
                'operating_margin_std': np.std(operating_margins) if operating_margins else 0,
                'margin_stable': (np.std(gross_margins) < 3) if gross_margins else False
            }
        except Exception as e:
            print(f"Error calculating margins: {e}")
            return {}
    
    def get_shares_outstanding_change(self):
        """Calculate share count change over 5 years"""
        try:
            info = self.stock.info
            shares_current = info.get('sharesOutstanding', 0)
            
            # Try to get historical shares outstanding
            # This is tricky - not directly available from yfinance
            # We'd need to parse balance sheets or use another source
            
            balance = self.stock.balance_sheet
            if balance.empty:
                return {'shares_5y_change': 0}
            
            # Get most recent and oldest available
            if len(balance.columns) >= 2:
                # Shares outstanding might be in balance sheet
                # Or we calculate from market cap / price
                pass
            
            return {'shares_5y_change': 0}  # Placeholder
        except:
            return {'shares_5y_change': 0}
    
    def get_debt_metrics(self):
        """Calculate debt metrics for leverage analysis"""
        try:
            info = self.stock.info
            balance = self.stock.balance_sheet
            income = self.stock.financials
            
            # Net Debt / EBITDA
            total_debt = info.get('totalDebt', 0)
            cash = info.get('totalCash', 0)
            net_debt = total_debt - cash
            ebitda = info.get('ebitda', 1)
            
            net_debt_ebitda = (net_debt / ebitda) if ebitda else 0
            
            # Interest Coverage
            if not income.empty:
                op_income_row = income.loc['Operating Income'] if 'Operating Income' in income.index else None
                interest_row = income.loc['Interest Expense'] if 'Interest Expense' in income.index else None
                
                if op_income_row is not None and interest_row is not None:
                    op_income = op_income_row.iloc[0]
                    interest = abs(interest_row.iloc[0])
                    interest_coverage = (op_income / interest) if interest else 999
                else:
                    interest_coverage = 5  # Default
            else:
                interest_coverage = 5
            
            return {
                'net_debt_ebitda': net_debt_ebitda,
                'interest_coverage': interest_coverage,
                'total_debt': total_debt,
                'net_debt': net_debt
            }
        except Exception as e:
            print(f"Error calculating debt metrics: {e}")
            return {}
    
    def get_company_age(self):
        """Try to get company founding/IPO dates"""
        try:
            # This is hard to get programmatically
            # Would need Wikipedia API or other source
            # For now, return 0 (will be manual field)
            return {'years_listed': 0, 'founded_year': None}
        except:
            return {'years_listed': 0, 'founded_year': None}
