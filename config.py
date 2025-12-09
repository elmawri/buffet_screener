"""
Configuration file for Buffett Qualitative Data Model
"""

# Your ticker list - update this with your 14 stocks
TICKERS = [
    "WLK",  # Westlake Corporation
    "ARW",  # Arrow Electronics
    "TSN",  # Tyson Foods
    "BIIB",  # Biogen Inc.
    "DD",  # DuPont de Nemours, Inc.
    "ELV",  # Elevance Health, Inc.
    "KMX",  # CarMax Inc
    "HUM",  # Humana Inc.
    "MOH",  # Molina Healthcare Inc
    "INTC",  # Intel Corporation
    "GOOG",  # Alphabet Inc.
    "AMZN",  # Amazon.com, Inc.
    "META",  # Meta Platforms, Inc.
    "TSLA",  # Tesla, Inc.
    "NVDA",  # NVIDIA Corporation
    "AAPL",  # Apple Inc.
    # Add your remaining 11 tickers here
]


# File paths
EXCEL_FILE = "Buffett_Qualitative_DataModel_Template.xlsx"
# API Keys - ADD YOUR KEYS HERE
USE_SEC_EDGAR = None
USE_FRED = None
USE_FMP = None

try:
    from config_local import *
except ImportError:
    ANTHROPIC_API_KEY = None
    FMP_API_KEY = None
    FRED_API_KEY = None



# Feature flags
USE_AI_ANALYSIS = True  # Set to False to disable AI analysis (will use faster heuristics)

# Data source settings
USE_CACHE = True  # Cache API responses to avoid rate limits
CACHE_EXPIRY_DAYS = 1  # How long to cache data

# Scoring thresholds (customize these based on your criteria)
SCORING_THRESHOLDS = {
    "ROE": {
        10: 25,  # ROE >= 25% gets score of 10
        9: 22,
        8: 20,
        7: 17,
        6: 15,
        5: 12,
        4: 10,
        3: 7,
        2: 5,
        1: 0
    },
    "ROIC": {
        10: 20,
        9: 18,
        8: 15,
        7: 13,
        6: 11,
        5: 9,
        4: 7,
        3: 5,
        2: 3,
        1: 0
    },
    # Add more scoring thresholds as needed
}

