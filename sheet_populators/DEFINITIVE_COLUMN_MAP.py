"""
DEFINITIVE COLUMN MAPPINGS - Based on actual Excel file analysis
DO NOT GUESS. These are the ACTUAL column numbers from the template.
Place this file in: buffett_screener/sheet_populators/
"""

# Column numbers (1-indexed for openpyxl)
COLUMNS = {
    'Tickers': {
        'Ticker': 1,              # A
        'Company': 2,             # B
        'ISIN': 3,                # C
        'CIK': 4,                 # D
        'Exchange': 5,            # E
        'Sector': 6,              # F
        'Industry': 7,            # G
        'Country': 8,             # H
        'Currency': 9,            # I
        'Primary_Source': 10,     # J
        'Include': 11,            # K
    },
    
    'Simplicity': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Segment_Count': 3,             # C
        'Segments_List': 4,             # D
        'Rev_Top_Segment': 5,           # E
        'Rev_Top2_Segments': 6,         # F
        'Geographic_Count': 7,          # G
        'Top_Geography': 8,             # H
        'Business_Model': 9,            # I
        'Complexity_Flags': 10,         # J
        'Accounting_Complexity': 11,    # K
        'Off_Balance_Exposures': 12,    # L
        'Products': 13,                 # M
        'Customers': 14,                # N
        'Supplier_Concentration': 15,   # O
        'Channel_Complexity': 16,       # P
        'Notes': 17,                    # Q
        'Score': 18,                    # R - ACTUAL SCORE COLUMN
        'Source': 19,                   # S
        'Last_Updated': 20,             # T
    },
    
    'OperatingHistory': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Founded_Year': 3,              # C
        'IPO_Year': 4,                  # D
        'Years_Since_IPO': 5,           # E
        'Years_Profitability': 6,       # F
        'Revenue_CAGR_10Y': 7,          # G
        'EPS_CAGR_10Y': 8,              # H
        'Rev_Down_Years': 9,            # I
        'EPS_Down_Years': 10,           # J
        'Restatements': 11,             # K
        'Strategy_Pivots': 12,          # L
        'Notes': 13,                    # M
        'Score': 14,                    # N - ACTUAL SCORE COLUMN
        'Source': 15,                   # O
        'Last_Updated': 16,             # P
    },
    
    'Moat': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Moat_Type': 3,                 # C
        'ROE_5Y_Avg': 4,                # D
        'ROIC_5Y_Avg': 5,               # E
        'Gross_Margin_5Y': 6,           # F
        'Operating_Margin_5Y': 7,       # G
        'Market_Share': 8,              # H
        'Market_Share_Trend': 9,        # I
        'Pricing_Power': 10,            # J
        'Patents_IP': 11,               # K
        'Switching_Costs': 12,          # L
        'Cost_Advantage': 13,           # M
        'Network_Effects': 14,          # N
        'Regulatory_Moat': 15,          # O
        'Notes': 16,                    # P
        'Score': 17,                    # Q - ACTUAL SCORE COLUMN
        'Source': 18,                   # R
        'Last_Updated': 19,             # S
    },
    
    'Management': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'CEO_Tenure': 3,                # C
        'CFO_Tenure': 4,                # D
        'Insider_Ownership': 5,         # E
        'Compensation': 6,              # F
        'Capital_Letters': 7,           # G
        'Disclosure_Quality': 8,        # H
        'Related_Party': 9,             # I
        'Accounting_Conservatism': 10,  # J
        'Share_Count_Change': 11,       # K
        'Buybacks_Below_IV': 12,        # L
        'MA_Discipline': 13,            # M
        'Dividend_Policy': 14,          # N
        'Notes': 15,                    # O
        'Score': 16,                    # P - ACTUAL SCORE COLUMN
        'Source': 17,                   # Q
        'Last_Updated': 18,             # R
    },
    
    'ROE_ROIC': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'ROE_TTM': 3,                   # C
        'ROE_5Y_Avg': 4,                # D
        'ROIC_TTM': 5,                  # E
        'ROIC_5Y_Avg': 6,               # F
        'FCF_Margin_5Y': 7,             # G
        'CapEx_Sales_5Y': 8,            # H
        'Notes': 9,                     # I
        'Score': 10,                    # J - ACTUAL SCORE COLUMN
        'Source': 11,                   # K
        'Last_Updated': 12,             # L
    },
    
    'Predictability': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'EPS_StdDev': 3,                # C
        'EPS_CAGR': 4,                  # D
        'Op_Margin_Avg': 5,             # E
        'Op_Margin_StdDev': 6,          # F
        'Revenue_StdDev': 7,            # G
        'Gross_Margin_Stability': 8,    # H
        'Earnings_Drawdown': 9,         # I
        'Guidance_Accuracy': 10,        # J
        'Notes': 11,                    # K
        'Score': 12,                    # L - ACTUAL SCORE COLUMN
        'Source': 13,                   # M
        'Last_Updated': 14,             # N
    },
    
    'CapitalAllocation': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Shares_Outstanding_Change': 3, # C
        'Net_Buyback_Yield': 4,         # D
        'Dividend_Payout': 5,           # E
        'Reinvestment_Rate': 6,         # F
        'Acquisition_Spend': 7,         # G
        'Post_MA_ROIC': 8,              # H
        'Debt_Issuance_vs_FCF': 9,      # I
        'Specials': 10,                 # J
        'Notes': 11,                    # K
        'Score': 12,                    # L - ACTUAL SCORE COLUMN
        'Source': 13,                   # M
        'Last_Updated': 14,             # N
    },
    
    'Leverage': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Debt_Equity_TTM': 3,           # C
        'Debt_Equity_5Y': 4,            # D
        'Interest_Coverage': 5,         # E
        'Net_Debt_EBITDA': 6,           # F
        'Cash': 7,                      # G
        'Debt_Maturity_2Y': 8,          # H
        'Debt_Maturity_2to5Y': 9,       # I
        'Debt_Maturity_5Y_Plus': 10,    # J
        'Liquidity_Facilities': 11,     # K
        'Covenant_Headroom': 12,        # L
        'Notes': 13,                    # M
        'Score': 14,                    # N - ACTUAL SCORE COLUMN
        'Source': 15,                   # O
        'Last_Updated': 16,             # P
    },
    
    'Resilience': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'Beta': 3,                      # C
        'Demand_Type': 4,               # D
        'Op_Margin_StdDev': 5,          # E
        'Rev_Change_2008': 6,           # F
        'Rev_Change_2020': 7,           # G
        'EPS_Change_2008': 8,           # H
        'EPS_Change_2020': 9,           # I
        'Dividend_Cuts': 10,            # J
        'Customer_Diversification': 11, # K
        'Supply_Chain_Risk': 12,        # L
        'Regulatory_Sensitivity': 13,   # M
        'Notes': 14,                    # N
        'Score': 15,                    # O - ACTUAL SCORE COLUMN
        'Source': 16,                   # P
        'Last_Updated': 17,             # Q
    },
    
    'PriceValue': {
        'Ticker': 1,                    # A
        'Company': 2,                   # B
        'PE_TTM': 3,                    # C
        'PE_10Y_Median': 4,             # D
        'PB_MRQ': 5,                    # E
        'PB_10Y_Median': 6,             # F
        'EV_EBIT_TTM': 7,               # G
        'EV_EBIT_10Y_Median': 8,        # H
        'P_FCF_TTM': 9,                 # I
        'P_FCF_10Y_Median': 10,         # J
        'Yield_vs_10Y': 11,             # K
        'IV_Discount': 12,              # L
        'Alt_Fair_Value': 13,           # M
        'Notes': 14,                    # N
        'Score': 15,                    # O - ACTUAL SCORE COLUMN
        'Source': 16,                   # P
        'Last_Updated': 17,             # Q
    },
}

# For Overview sheet formulas - these point to the SCORE columns in each sheet
OVERVIEW_SCORE_REFS = {
    'Simplicity': 'R',          # Col 18
    'OperatingHistory': 'N',    # Col 14
    'Moat': 'Q',                # Col 17
    'Management': 'P',          # Col 16
    'ROE_ROIC': 'J',            # Col 10
    'Predictability': 'L',      # Col 12
    'CapitalAllocation': 'L',   # Col 12
    'Leverage': 'N',            # Col 14
    'Resilience': 'O',          # Col 15
    'PriceValue': 'O',          # Col 15
}

# For Overview sheet - correct Tickers column references
OVERVIEW_TICKERS_REFS = {
    'Sector': 'F',      # Col 6 (NOT C!)
    'Industry': 'G',    # Col 7 (NOT D!)
    'Country': 'H',     # Col 8 (NOT J!)
}
