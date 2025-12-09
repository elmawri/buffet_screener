# Buffett Qualitative Data Model - Automated Screener

## 📁 Folder Structure

```
buffett_screener/
│
├── Buffett_Qualitative_DataModel_Template.xlsx  # Your working Excel file
├── config.py                                     # Configuration (tickers, settings)
├── requirements.txt                              # Python dependencies
├── README.md                                     # This file
│
├── data_fetchers/                                # Data collection modules
│   ├── __init__.py
│   ├── utils.py                                  # Helper functions
│   └── yahoo_finance.py                          # Yahoo Finance API wrapper
│
├── sheet_populators/                             # One script per Excel sheet
│   ├── __init__.py
│   ├── populate_tickers.py                       # ✅ Ready to use
│   ├── populate_roe_roic.py                      # Coming next
│   ├── populate_leverage.py                      # Coming next
│   ├── populate_operating_history.py             # Coming next
│   └── ... (more to be added)
│
└── scoring/                                      # Scoring algorithms
    ├── __init__.py
    └── ... (to be added)
```

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
cd buffett_screener
pip install -r requirements.txt --break-system-packages
```

### 2. Configure Your Tickers
Edit `config.py` and add your ticker list:
```python
TICKERS = ["AAPL", "MSFT", "GOOGL", ...]
```

### 3. Run Individual Sheet Populators
```bash
# Populate Tickers sheet
python sheet_populators/populate_tickers.py

# Or test with specific tickers
python sheet_populators/populate_tickers.py AAPL MSFT
```

## 📊 Current Status

### Phase 1: Fully Automatable Sheets (In Progress)
- ✅ **Tickers** - Basic company info (READY)
- 🔨 **ROE_ROIC** - Return metrics (NEXT)
- 🔨 **Leverage** - Debt metrics (NEXT)
- 🔨 **Operating History** - Historical financials (NEXT)
- 🔨 **Price Value** - Valuation ratios (NEXT)

### Phase 2: Partially Automatable (Future)
- ⏳ Management, Moat, Capital Allocation, etc.

### Phase 3: Manual Input Required
- ⏳ Simplicity, qualitative assessments

## 🔧 Development Workflow

1. Each sheet has its own populator script in `sheet_populators/`
2. All scripts use shared data fetchers from `data_fetchers/`
3. Run scripts individually as they're developed
4. Eventually we'll create `run_all.py` to orchestrate everything

## 📝 Notes

- Scripts automatically update `Last Updated` dates
- Data is cached to avoid API rate limits
- Failed fetches are logged but don't stop execution
- Always backup your Excel file before running scripts!

## 🐛 Troubleshooting

If you get errors:
1. Check your ticker symbols are correct
2. Ensure you have internet connection
3. Yahoo Finance may occasionally be slow - retry if needed
4. Check the console output for specific error messages
