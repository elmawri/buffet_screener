"""
DEFINITIVE COLUMN MAPPINGS - Reference for All Populators
This is the single source of truth for column numbers
"""

# Column mappings for each sheet
COLUMN_MAP = {
    'Tickers': {
        'Ticker': 1,
        'Company': 2,
        'ISIN': 3,
        'CIK': 4,
        'Exchange': 5,
        'Sector': 6,
        'Industry': 7,
        'Country': 8,
        'Currency': 9,
        'Primary_Source': 10,
        'Include': 11
    },
    
    'Simplicity': {
        'Ticker': 1,
        'Company': 2,
        'Segment_Count': 3,
        'Segments_List': 4,
        'Rev_Top_Segment_Pct': 5,
        'Rev_Top2_Segments_Pct': 6,
        'Geographic_Count': 7,
        'Top_Geography_Pct': 8,
        'Business_Model': 9,
        'Complexity_Flags': 10,
        'Accounting_Complexity': 11,
        'Off_Balance_Exposures': 12,
        'Products': 13,
        'Customers': 14,
        'Supplier_Concentration': 15,
        'Channel_Complexity': 16,
        'Notes': 17,
        'Score': 18,
        'Source': 19,
        'Last_Updated': 20
    },
    
    'OperatingHistory': {
        'Ticker': 1,
        'Company': 2,
        'Founded_Year': 3,
        'IPO_Year': 4,
        'Years_Since_IPO': 5,
        'Years_Profitability': 6,
        'Revenue_10Y_CAGR': 7,
        'EPS_10Y_CAGR': 8,
        'Rev_Down_Years': 9,
        'EPS_Down_Years': 10,
        'Restatements': 11,
        'Major_Pivots': 12,
        'Notes': 13,
        'Score': 14,
        'Source': 15,
        'Last_Updated': 16
    },
    
    'Moat': {
        'Ticker': 1,
        'Company': 2,
        'Moat_Type': 3,
        'ROE_5Y_Avg': 4,
        'ROIC_5Y_Avg': 5,
        'Gross_Margin_5Y_Avg': 6,
        'Operating_Margin_5Y_Avg': 7,
        'Market_Share_Pct': 8,
        'Market_Share_Trend': 9,
        'Pricing_Power': 10,
        'Patents_IP': 11,
        'Switching_Costs': 12,
        'Cost_Advantage': 13,
        'Network_Effects': 14,
        'Reg_License_Moat': 15,
        'Notes': 16,
        'Score': 17,
        'Source': 18,
        'Last_Updated': 19
    },
    
    'Management': {
        'Ticker': 1,
        'Company': 2,
        'CEO_Tenure': 3,
        'CFO_Tenure': 4,
        'Insider_Ownership_Pct': 5,
        'Compensation_Alignment': 6,
        'Capital_Allocation_Letters': 7,
        'Disclosure_Quality': 8,
        'Related_Party_Risks': 9,
        'Accounting_Conservatism': 10,
        'Share_Count_5Y_Change': 11,
        'Buybacks_Below_IV': 12,
        'MA_Discipline': 13,
        'Dividend_Policy': 14,
        'Notes': 15,
        'Score': 16,
        'Source': 17,
        'Last_Updated': 18
    },
    
    'ROE_ROIC': {
        'Ticker': 1,
        'Company': 2,
        'ROE_TTM': 3,
        'ROE_5Y_Avg': 4,
        'ROIC_TTM': 5,
        'ROIC_5Y_Avg': 6,
        'FCF_Margin_5Y_Avg': 7,
        'CapEx_Sales_5Y_Avg': 8,
        'Notes': 9,
        'Score': 10,
        'Source': 11,
        'Last_Updated': 12
    },
    
    'Predictability': {
        'Ticker': 1,
        'Company': 2,
        'EPS_10Y_StdDev': 3,
        'EPS_10Y_CAGR': 4,
        'Operating_Margin_10Y_Avg': 5,
        'Operating_Margin_10Y_StdDev': 6,
        'Revenue_10Y_StdDev': 7,
        'Gross_Margin_Stability': 8,
        'Earnings_Drawdown': 9,
        'Guidance_Accuracy': 10,
        'Notes': 11,
        'Score': 12,
        'Source': 13,
        'Last_Updated': 14
    },
    
    'CapitalAllocation': {
        'Ticker': 1,
        'Company': 2,
        'Shares_Outstanding_5Y_Change': 3,
        'Net_Buyback_Yield': 4,
        'Dividend_Payout_Ratio': 5,
        'Reinvestment_Rate': 6,
        'Acquisition_Spend_5Y': 7,
        'Post_MA_ROIC': 8,
        'Debt_Issuance_vs_FCF': 9,
        'Specials_One_Offs': 10,
        'Notes': 11,
        'Score': 12,
        'Source': 13,
        'Last_Updated': 14
    },
    
    'Leverage': {
        'Ticker': 1,
        'Company': 2,
        'Debt_Equity_TTM': 3,
        'Debt_Equity_5Y_Avg': 4,
        'Interest_Coverage': 5,
        'Net_Debt_EBITDA': 6,
        'Cash_Equivalents': 7,
        'Debt_Maturity_Under_2Y': 8,
        'Debt_Maturity_2_5Y': 9,
        'Debt_Maturity_Over_5Y': 10,
        'Liquidity_Facilities': 11,
        'Covenant_Headroom': 12,
        'Notes': 13,
        'Score': 14,
        'Source': 15,
        'Last_Updated': 16
    },
    
    'Resilience': {
        'Ticker': 1,
        'Company': 2,
        'Beta_5Y': 3,
        'Demand_Type': 4,
        'Op_Margin_10Y_StdDev': 5,
        'Revenue_Change_2008_09': 6,
        'Revenue_Change_2020': 7,
        'EPS_Change_2008_09': 8,
        'EPS_Change_2020': 9,
        'Dividend_Cuts_Crises': 10,
        'Customer_Diversification': 11,
        'Supply_Chain_Risk': 12,
        'Regulatory_Sensitivity': 13,
        'Notes': 14,
        'Score': 15,
        'Source': 16,
        'Last_Updated': 17
    },
    
    'PriceValue': {
        'Ticker': 1,
        'Company': 2,
        'PE_TTM': 3,
        'PE_10Y_Median': 4,
        'PB_MRQ': 5,
        'PB_10Y_Median': 6,
        'EV_EBIT_TTM': 7,
        'EV_EBIT_10Y_Median': 8,
        'P_FCF_TTM': 9,
        'P_FCF_10Y_Median': 10,
        'Yield_vs_10Y_UST': 11,
        'Implied_IV_Discount': 12,
        'Alt_Fair_Value': 13,
        'Notes': 14,
        'Score': 15,
        'Source': 16,
        'Last_Updated': 17
    },
    
    'Overview': {
        'Ticker': 1,
        'Company': 2,
        'Sector': 3,
        'Industry': 4,
        'Country': 5,
        'Notes': 6,
        'Simplicity_Score': 7,
        'OperatingHistory_Score': 8,
        'Moat_Score': 9,
        'Management_Score': 10,
        'ROE_ROIC_Score': 11,
        'Predictability_Score': 12,
        'CapitalAllocation_Score': 13,
        'Leverage_Score': 14,
        'Resilience_Score': 15,
        'PriceValue_Score': 16,
        'Total': 17,
        'Average': 18,
        'Rank': 19
    }
}

# Helper function to get column number
def get_col(sheet_name, field_name):
    """Get column number for a field in a sheet"""
    return COLUMN_MAP.get(sheet_name, {}).get(field_name, None)
