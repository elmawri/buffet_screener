@echo off
echo ================================================================================
echo BUFFETT QUALITATIVE DATA MODEL - AUTOMATED SCREENER
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install_dependencies.bat first
    pause
    exit /b 1
)

REM Check if config has tickers
python -c "from config import TICKERS; exit(0 if TICKERS else 1)" 2>nul
if errorlevel 1 (
    echo ERROR: No tickers found in config.py
    echo.
    echo Please edit config.py and add your ticker list to the TICKERS variable.
    echo Example: TICKERS = ["AAPL", "MSFT", "GOOGL"]
    echo.
    pause
    exit /b 1
)

echo Starting data collection...
echo This will populate all sheets with financial data from Yahoo Finance
echo.
echo Press Ctrl+C to cancel, or
pause

python run_all.py

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo ERRORS OCCURRED during execution
    echo ================================================================================
    echo Please check the messages above for details
    echo.
) else (
    echo.
    echo ================================================================================
    echo COMPLETED SUCCESSFULLY!
    echo ================================================================================
    echo.
    echo Your Excel file has been updated with the latest data.
    echo Please open: Buffett_Qualitative_DataModel_Template.xlsx
    echo.
)

pause
