"""
AUTOMATIC POPULATOR UPDATER
This script automatically updates all your existing populator files to use the correct column mappings.
"""

import os
import re
import shutil
from pathlib import Path

# Files to update
POPULATOR_FILES = [
    'populate_tickers.py',
    'populate_simplicity.py',
    'populate_operating_history.py',
    'populate_moat.py',
    'populate_management.py',
    'populate_roe_roic.py',
    'populate_predictability.py',
    'populate_capital_allocation.py',
    'populate_leverage.py',
    'populate_resilience.py',
    'populate_price_value.py',
    'populate_overview.py',
]

# Map file names to sheet names in DEFINITIVE_COLUMN_MAP
FILE_TO_SHEET = {
    'populate_tickers.py': 'Tickers',
    'populate_simplicity.py': 'Simplicity',
    'populate_operating_history.py': 'OperatingHistory',
    'populate_moat.py': 'Moat',
    'populate_management.py': 'Management',
    'populate_roe_roic.py': 'ROE_ROIC',
    'populate_predictability.py': 'Predictability',
    'populate_capital_allocation.py': 'CapitalAllocation',
    'populate_leverage.py': 'Leverage',
    'populate_resilience.py': 'Resilience',
    'populate_price_value.py': 'PriceValue',
    'populate_overview.py': 'Overview',
}

# Common column number patterns to replace
# Format: (pattern, replacement_template)
COLUMN_PATTERNS = {
    'Tickers': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['ISIN']",
        4: "cols['CIK']",
        5: "cols['Exchange']",
        6: "cols['Sector']",
        7: "cols['Industry']",
        8: "cols['Country']",
        9: "cols['Currency']",
        10: "cols['Primary_Source']",
        11: "cols['Include']",
    },
    'Simplicity': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Segment_Count']",
        4: "cols['Segments_List']",
        5: "cols['Rev_Top_Segment']",
        6: "cols['Rev_Top2_Segments']",
        7: "cols['Geographic_Count']",
        8: "cols['Top_Geography']",
        9: "cols['Business_Model']",
        10: "cols['Complexity_Flags']",
        11: "cols['Accounting_Complexity']",
        12: "cols['Off_Balance_Exposures']",
        13: "cols['Products']",
        14: "cols['Customers']",
        15: "cols['Supplier_Concentration']",
        16: "cols['Channel_Complexity']",
        17: "cols['Notes']",
        18: "cols['Score']",
        19: "cols['Source']",
        20: "cols['Last_Updated']",
    },
    'OperatingHistory': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Founded_Year']",
        4: "cols['IPO_Year']",
        5: "cols['Years_Since_IPO']",
        6: "cols['Years_Profitability']",
        7: "cols['Revenue_CAGR_10Y']",
        8: "cols['EPS_CAGR_10Y']",
        9: "cols['Rev_Down_Years']",
        10: "cols['EPS_Down_Years']",
        11: "cols['Restatements']",
        12: "cols['Strategy_Pivots']",
        13: "cols['Notes']",
        14: "cols['Score']",
        15: "cols['Source']",
        16: "cols['Last_Updated']",
    },
    'Moat': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Moat_Type']",
        4: "cols['ROE_5Y_Avg']",
        5: "cols['ROIC_5Y_Avg']",
        6: "cols['Gross_Margin_5Y']",
        7: "cols['Operating_Margin_5Y']",
        8: "cols['Market_Share']",
        9: "cols['Market_Share_Trend']",
        10: "cols['Pricing_Power']",
        11: "cols['Patents_IP']",
        12: "cols['Switching_Costs']",
        13: "cols['Cost_Advantage']",
        14: "cols['Network_Effects']",
        15: "cols['Regulatory_Moat']",
        16: "cols['Notes']",
        17: "cols['Score']",
        18: "cols['Source']",
        19: "cols['Last_Updated']",
    },
    'Management': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['CEO_Tenure']",
        4: "cols['CFO_Tenure']",
        5: "cols['Insider_Ownership']",
        6: "cols['Compensation']",
        7: "cols['Capital_Letters']",
        8: "cols['Disclosure_Quality']",
        9: "cols['Related_Party']",
        10: "cols['Accounting_Conservatism']",
        11: "cols['Share_Count_Change']",
        12: "cols['Buybacks_Below_IV']",
        13: "cols['MA_Discipline']",
        14: "cols['Dividend_Policy']",
        15: "cols['Notes']",
        16: "cols['Score']",
        17: "cols['Source']",
        18: "cols['Last_Updated']",
    },
    'ROE_ROIC': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['ROE_TTM']",
        4: "cols['ROE_5Y_Avg']",
        5: "cols['ROIC_TTM']",
        6: "cols['ROIC_5Y_Avg']",
        7: "cols['FCF_Margin_5Y']",
        8: "cols['CapEx_Sales_5Y']",
        9: "cols['Notes']",
        10: "cols['Score']",
        11: "cols['Source']",
        12: "cols['Last_Updated']",
    },
    'Predictability': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['EPS_StdDev']",
        4: "cols['EPS_CAGR']",
        5: "cols['Op_Margin_Avg']",
        6: "cols['Op_Margin_StdDev']",
        7: "cols['Revenue_StdDev']",
        8: "cols['Gross_Margin_Stability']",
        9: "cols['Earnings_Drawdown']",
        10: "cols['Guidance_Accuracy']",
        11: "cols['Notes']",
        12: "cols['Score']",
        13: "cols['Source']",
        14: "cols['Last_Updated']",
    },
    'CapitalAllocation': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Shares_Outstanding_Change']",
        4: "cols['Net_Buyback_Yield']",
        5: "cols['Dividend_Payout']",
        6: "cols['Reinvestment_Rate']",
        7: "cols['Acquisition_Spend']",
        8: "cols['Post_MA_ROIC']",
        9: "cols['Debt_Issuance_vs_FCF']",
        10: "cols['Specials']",
        11: "cols['Notes']",
        12: "cols['Score']",
        13: "cols['Source']",
        14: "cols['Last_Updated']",
    },
    'Leverage': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Debt_Equity_TTM']",
        4: "cols['Debt_Equity_5Y']",
        5: "cols['Interest_Coverage']",
        6: "cols['Net_Debt_EBITDA']",
        7: "cols['Cash']",
        8: "cols['Debt_Maturity_2Y']",
        9: "cols['Debt_Maturity_2to5Y']",
        10: "cols['Debt_Maturity_5Y_Plus']",
        11: "cols['Liquidity_Facilities']",
        12: "cols['Covenant_Headroom']",
        13: "cols['Notes']",
        14: "cols['Score']",
        15: "cols['Source']",
        16: "cols['Last_Updated']",
    },
    'Resilience': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['Beta']",
        4: "cols['Demand_Type']",
        5: "cols['Op_Margin_StdDev']",
        6: "cols['Rev_Change_2008']",
        7: "cols['Rev_Change_2020']",
        8: "cols['EPS_Change_2008']",
        9: "cols['EPS_Change_2020']",
        10: "cols['Dividend_Cuts']",
        11: "cols['Customer_Diversification']",
        12: "cols['Supply_Chain_Risk']",
        13: "cols['Regulatory_Sensitivity']",
        14: "cols['Notes']",
        15: "cols['Score']",
        16: "cols['Source']",
        17: "cols['Last_Updated']",
    },
    'PriceValue': {
        1: "cols['Ticker']",
        2: "cols['Company']",
        3: "cols['PE_TTM']",
        4: "cols['PE_10Y_Median']",
        5: "cols['PB_MRQ']",
        6: "cols['PB_10Y_Median']",
        7: "cols['EV_EBIT_TTM']",
        8: "cols['EV_EBIT_10Y_Median']",
        9: "cols['P_FCF_TTM']",
        10: "cols['P_FCF_10Y_Median']",
        11: "cols['Yield_vs_10Y']",
        12: "cols['IV_Discount']",
        13: "cols['Alt_Fair_Value']",
        14: "cols['Notes']",
        15: "cols['Score']",
        16: "cols['Source']",
        17: "cols['Last_Updated']",
    },
}

def backup_file(filepath):
    """Create a backup of the original file"""
    backup_path = f"{filepath}.backup"
    shutil.copy2(filepath, backup_path)
    return backup_path

def has_column_map_import(content):
    """Check if file already imports COLUMNS"""
    return 'from DEFINITIVE_COLUMN_MAP import COLUMNS' in content or \
           'from column_mappings import COLUMN_MAP' in content

def add_import_statement(content):
    """Add the import statement if not present"""
    if has_column_map_import(content):
        return content
    
    # Find the last import statement
    lines = content.split('\n')
    last_import_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            last_import_idx = i
    
    # Insert after last import
    if last_import_idx >= 0:
        lines.insert(last_import_idx + 1, 'from DEFINITIVE_COLUMN_MAP import COLUMNS')
    else:
        # No imports found, add at top after docstring
        insert_idx = 0
        if lines[0].strip().startswith('"""') or lines[0].strip().startswith("'''"):
            # Skip docstring
            for i in range(1, len(lines)):
                if '"""' in lines[i] or "'''" in lines[i]:
                    insert_idx = i + 1
                    break
        lines.insert(insert_idx, 'from DEFINITIVE_COLUMN_MAP import COLUMNS')
    
    return '\n'.join(lines)

def add_cols_variable(content, sheet_name):
    """Add cols = COLUMNS['SheetName'] at the start of populate function"""
    # Find the populate function
    pattern = r'(def populate_\w+\([^)]+\):)'
    
    def replacer(match):
        func_def = match.group(1)
        # Add cols variable on next line with proper indentation
        return f"{func_def}\n    cols = COLUMNS['{sheet_name}']"
    
    # Only add if not already present
    if f"cols = COLUMNS['{sheet_name}']" not in content:
        content = re.sub(pattern, replacer, content)
    
    return content

def replace_column_numbers(content, sheet_name):
    """Replace hardcoded column numbers with cols['FieldName']"""
    if sheet_name not in COLUMN_PATTERNS:
        return content
    
    mappings = COLUMN_PATTERNS[sheet_name]
    
    # Pattern: column=NUMBER) where NUMBER is a digit
    # We need to be careful to only replace in ws.cell contexts
    for col_num, col_name in mappings.items():
        # Pattern: column=NUMBER) or column=NUMBER,
        pattern1 = rf'column={col_num}\)'
        pattern2 = rf'column={col_num},'
        
        replacement1 = f'column={col_name})'
        replacement2 = f'column={col_name},'
        
        content = re.sub(pattern1, replacement1, content)
        content = re.sub(pattern2, replacement2, content)
    
    return content

def update_file(filepath, sheet_name):
    """Update a single populator file"""
    print(f"\nUpdating {filepath}...")
    
    # Read original content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup original
    backup_path = backup_file(filepath)
    print(f"  ✓ Backup created: {backup_path}")
    
    # Apply transformations
    content = add_import_statement(content)
    print(f"  ✓ Added import statement")
    
    content = add_cols_variable(content, sheet_name)
    print(f"  ✓ Added cols variable")
    
    content = replace_column_numbers(content, sheet_name)
    print(f"  ✓ Replaced column numbers with mapped names")
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ File updated successfully!")

def update_all_populators(directory):
    """Update all populator files in the directory"""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    # Check if DEFINITIVE_COLUMN_MAP.py exists
    column_map_path = directory / 'DEFINITIVE_COLUMN_MAP.py'
    if not column_map_path.exists():
        print(f"Error: DEFINITIVE_COLUMN_MAP.py not found in {directory}")
        print("Please copy it there first!")
        return
    
    updated_count = 0
    skipped_count = 0
    
    print("=" * 80)
    print("AUTOMATIC POPULATOR UPDATER")
    print("=" * 80)
    
    for filename in POPULATOR_FILES:
        filepath = directory / filename
        
        if not filepath.exists():
            print(f"\nSkipping {filename} - file not found")
            skipped_count += 1
            continue
        
        sheet_name = FILE_TO_SHEET[filename]
        
        try:
            update_file(filepath, sheet_name)
            updated_count += 1
        except Exception as e:
            print(f"  ✗ Error updating {filename}: {e}")
            skipped_count += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files updated: {updated_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"\nAll original files backed up with .backup extension")
    print(f"Review the changes and test before deleting backups!")

if __name__ == "__main__":
    import sys
    import os
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Use current directory by default (should be sheet_populators folder)
        directory = os.getcwd()
    
    print(f"Looking for populator files in: {directory}")
    print(f"Make sure DEFINITIVE_COLUMN_MAP.py is in this same directory!\n")
    print(f"NOTE: Run this script FROM INSIDE the sheet_populators folder:")
    print(f"  cd sheet_populators")
    print(f"  python auto_update_populators.py\n")
    
    update_all_populators(directory)
