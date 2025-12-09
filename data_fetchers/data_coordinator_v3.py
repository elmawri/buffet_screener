"""
Data Coordinator V3 - FINAL PRODUCTION VERSION
6-Phase Optimal Sequence with Yahoo as Comprehensive Gap-Filler

Sequence:
1. Yahoo Basic (ISIN, CIK)
2. Edgar (Segments, Executives)
3. FMP (10Y Historicals)
4. FRED (Treasury)
5. Yahoo Gap-Fill (Fill remaining empty fields)
6. AI Analysis (With complete context)
"""
from typing import Dict, Optional
from datetime import datetime
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_fetchers.yahoo_finance import YahooFinanceFetcher
from data_fetchers.sec_edgar import SECEdgarFetcher
from data_fetchers.fmp import FMPFetcher
from data_fetchers.ai_analyzer import AIAnalyzer
from data_fetchers.third_sources import FREDFetcher

class DataCoordinatorV3:
    """
    Production-ready coordinator with optimal 6-phase sequence
    Yahoo serves dual role: initialization + comprehensive fallback
    """
    
    def __init__(self, ticker: str, anthropic_key: Optional[str] = None,
                 fmp_key: Optional[str] = None, fred_key: Optional[str] = None):
        self.ticker = ticker
        
        # Initialize fetchers
        self.yahoo = YahooFinanceFetcher(ticker)
        self.fmp = FMPFetcher(fmp_key) if fmp_key else None
        self.ai = AIAnalyzer(anthropic_key) if anthropic_key else None
        self.fred = FREDFetcher(fred_key) if fred_key else None
        self.edgar = None
        
        # Data storage by phase
        self._phase1_basic = None
        self._phase2_edgar = None
        self._phase3_fmp = None
        self._phase4_fred = None
        self._phase5_yahoo_fallback = {}  # Gap-fill data
        self._phase6_ai = None
        
        self._initialized = False
    
    def get_all_data(self) -> Dict:
        """
        MASTER METHOD: Execute all 6 phases in optimal order
        Returns comprehensive data with maximum completeness
        """
        print(f"\n{'='*80}")
        print(f"DATA COORDINATOR V3: {self.ticker}")
        print(f"{'='*80}")
        print("6-Phase Optimal Sequence:")
        print("  1. Yahoo Basic (ISIN, CIK, Description)")
        print("  2. Edgar (Segments, Executives, Debt)")
        print("  3. FMP (10Y Historicals, Medians)")
        print("  4. FRED (Treasury Yields)")
        print("  5. Yahoo Gap-Fill (Fill remaining empty fields)")
        print("  6. AI Analysis (With complete context)")
        print(f"{'='*80}\n")
        
        # Execute all phases
        self._phase1_initialize_basic()
        self._phase2_fetch_edgar()
        self._phase3_fetch_fmp()
        self._phase4_fetch_fred()
        self._phase5_fill_gaps_yahoo()  # ⭐ NEW!
        self._phase6_run_ai()
        
        # Compile and return
        return self._compile_results()
    
    def _phase1_initialize_basic(self):
        """PHASE 1: Get basic info from Yahoo (ISIN, CIK, description)"""
        print(f"\n{'='*60}")
        print("PHASE 1: Yahoo Basic Info")
        print(f"{'='*60}")
        
        info = self.yahoo.get_info()
        
        # Extract ISIN
        isin = info.get('isin', '')
        if not isin:
            import yfinance as yf
            stock = yf.Ticker(self.ticker)
            if hasattr(stock, 'isin'):
                isin = stock.isin
        
        # Extract CIK
        cik = info.get('cik', '')
        
        self._phase1_basic = {
            'ticker': self.ticker,
            'company_name': info.get('longName', info.get('shortName')),
            'isin': isin,
            'cik': cik,
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'country': info.get('country'),
            'description': info.get('longBusinessSummary', ''),
            'full_info': info  # Store for Phase 5 gap-fill
        }
        
        print(f"  ✅ Ticker: {self.ticker}")
        print(f"  ✅ ISIN: {isin if isin else '❌ Not found'}")
        print(f"  ✅ CIK: {cik if cik else '❌ Not found'}")
        
        # Initialize Edgar if CIK available
        if cik:
            self.edgar = SECEdgarFetcher(cik)
            print(f"  ✅ Edgar initialized with CIK")
        else:
            print(f"  ⚠️  No CIK - Edgar disabled")
        
        self._initialized = True
    
    def _phase2_fetch_edgar(self):
        """PHASE 2: Fetch Edgar data (uses CIK from Phase 1)"""
        print(f"\n{'='*60}")
        print("PHASE 2: SEC Edgar Data")
        print(f"{'='*60}")
        
        if not self.edgar:
            print("  ⏭️  Skipped (no CIK available)")
            self._phase2_edgar = {}
            return
        
        self._phase2_edgar = self.edgar.get_comprehensive_data()
        
        # Report what was found
        if self._phase2_edgar.get('segments'):
            seg_count = self._phase2_edgar['segments'].get('segment_count', 0)
            print(f"  ✅ Segments: {seg_count}")
        
        if self._phase2_edgar.get('history', {}).get('founded_year'):
            print(f"  ✅ Founded: {self._phase2_edgar['history']['founded_year']}")
        
        if self._phase2_edgar.get('executives', {}).get('ceo', {}).get('tenure_years'):
            tenure = self._phase2_edgar['executives']['ceo']['tenure_years']
            print(f"  ✅ CEO Tenure: {tenure} years")
    
    def _phase3_fetch_fmp(self):
        """PHASE 3: Fetch FMP data"""
        print(f"\n{'='*60}")
        print("PHASE 3: FMP Historical Data")
        print(f"{'='*60}")
        
        if not self.fmp:
            print("  ⏭️  Skipped (no API key)")
            self._phase3_fmp = {}
            return
        
        self._phase3_fmp = self.fmp.get_comprehensive_data(self.ticker)
        
        # Report key metrics
        metrics = self._phase3_fmp.get('metrics_10y', {})
        if metrics.get('roe', {}).get('avg_10y'):
            print(f"  ✅ ROE 10Y Avg: {metrics['roe']['avg_10y']:.1f}%")
        if metrics.get('valuation', {}).get('pe_median_10y'):
            print(f"  ✅ P/E 10Y Median: {metrics['valuation']['pe_median_10y']:.1f}")
    
    def _phase4_fetch_fred(self):
        """PHASE 4: Fetch FRED data"""
        print(f"\n{'='*60}")
        print("PHASE 4: FRED Economic Data")
        print(f"{'='*60}")
        
        if not self.fred:
            print("  ⏭️  Skipped (no API key)")
            self._phase4_fred = {}
            return
        
        treasury = self.fred.get_treasury_10y_yield()
        self._phase4_fred = {'treasury_10y': treasury}
        
        if treasury:
            print(f"  ✅ 10Y Treasury: {treasury:.2f}%")
    
    def _phase5_fill_gaps_yahoo(self):
        """
        PHASE 5: Yahoo Gap-Fill ⭐ NEW!
        Fill any remaining empty fields with Yahoo data
        """
        print(f"\n{'='*60}")
        print("PHASE 5: Yahoo Gap-Fill")
        print(f"{'='*60}")
        print("  Checking for missing fields...")
        
        gaps_filled = 0
        info = self._phase1_basic.get('full_info', {})
        
        # Check and fill ROE 5Y Average
        fmp_roe = self._phase3_fmp.get('metrics_10y', {}).get('roe', {}).get('avg_5y')
        if not fmp_roe:
            # Calculate from Yahoo if possible
            roe_ttm = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
            if roe_ttm:
                self._phase5_yahoo_fallback['roe_5y_avg'] = roe_ttm  # Use TTM as fallback
                print(f"  → Filled ROE 5Y (Yahoo TTM): {roe_ttm:.1f}%")
                gaps_filled += 1
        
        # Check and fill ROIC 5Y Average
        fmp_roic = self._phase3_fmp.get('metrics_10y', {}).get('roic', {}).get('avg_5y')
        if not fmp_roic:
            # Estimate ROIC from ROE
            roe = info.get('returnOnEquity', 0)
            if roe:
                roic_estimate = roe * 0.7 * 100  # Rough estimate
                self._phase5_yahoo_fallback['roic_5y_avg'] = roic_estimate
                print(f"  → Filled ROIC 5Y (Yahoo estimate): {roic_estimate:.1f}%")
                gaps_filled += 1
        
        # Check and fill Gross Margin 5Y
        fmp_gross = self._phase3_fmp.get('metrics_10y', {}).get('margins', {}).get('gross_avg_5y')
        if not fmp_gross:
            gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
            if gross_margin:
                self._phase5_yahoo_fallback['gross_margin_5y'] = gross_margin
                print(f"  → Filled Gross Margin 5Y (Yahoo TTM): {gross_margin:.1f}%")
                gaps_filled += 1
        
        # Check and fill Operating Margin 5Y
        fmp_op = self._phase3_fmp.get('metrics_10y', {}).get('margins', {}).get('operating_avg_5y')
        if not fmp_op:
            op_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
            if op_margin:
                self._phase5_yahoo_fallback['operating_margin_5y'] = op_margin
                print(f"  → Filled Operating Margin 5Y (Yahoo TTM): {op_margin:.1f}%")
                gaps_filled += 1
        
        # Check and fill P/E Median
        fmp_pe_med = self._phase3_fmp.get('metrics_10y', {}).get('valuation', {}).get('pe_median_10y')
        if not fmp_pe_med:
            pe_ttm = info.get('trailingPE')
            if pe_ttm:
                self._phase5_yahoo_fallback['pe_median'] = pe_ttm  # Use current as proxy
                print(f"  → Filled P/E Median (Yahoo TTM): {pe_ttm:.1f}")
                gaps_filled += 1
        
        # Check and fill P/B Median
        fmp_pb_med = self._phase3_fmp.get('metrics_10y', {}).get('valuation', {}).get('pb_median_10y')
        if not fmp_pb_med:
            pb_mrq = info.get('priceToBook')
            if pb_mrq:
                self._phase5_yahoo_fallback['pb_median'] = pb_mrq
                print(f"  → Filled P/B Median (Yahoo MRQ): {pb_mrq:.1f}")
                gaps_filled += 1
        
        # Check and fill Revenue/EPS Growth
        fmp_rev_cagr = self._phase3_fmp.get('metrics_10y', {}).get('growth', {}).get('revenue_cagr_10y')
        if not fmp_rev_cagr:
            rev_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
            if rev_growth:
                self._phase5_yahoo_fallback['revenue_growth'] = rev_growth
                print(f"  → Filled Revenue Growth (Yahoo TTM): {rev_growth:.1f}%")
                gaps_filled += 1
        
        fmp_eps_cagr = self._phase3_fmp.get('metrics_10y', {}).get('growth', {}).get('eps_cagr_10y')
        if not fmp_eps_cagr:
            earnings_growth = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else None
            if earnings_growth:
                self._phase5_yahoo_fallback['earnings_growth'] = earnings_growth
                print(f"  → Filled EPS Growth (Yahoo TTM): {earnings_growth:.1f}%")
                gaps_filled += 1
        
        # Crisis performance fallback (use Beta as volatility proxy)
        fmp_crisis = self._phase3_fmp.get('crisis_performance', {})
        if not fmp_crisis.get('2008_2009'):
            beta = info.get('beta')
            if beta:
                # High beta = more volatile in crises
                self._phase5_yahoo_fallback['crisis_volatility_proxy'] = beta
                print(f"  → Using Beta as crisis proxy: {beta:.2f}")
                gaps_filled += 1
        
        if gaps_filled == 0:
            print("  ✅ No gaps found - all fields filled by Edgar/FMP")
        else:
            print(f"\n  ✅ Filled {gaps_filled} gaps with Yahoo data")
    
    def _phase6_run_ai(self):
        """PHASE 6: AI Analysis with complete context"""
        print(f"\n{'='*60}")
        print("PHASE 6: AI Analysis (Full Context)")
        print(f"{'='*60}")
        
        if not self.ai or not self.ai.enabled:
            print("  ⏭️  Skipped (AI disabled)")
            self._phase6_ai = {}
            return
        
        description = self._phase1_basic.get('description', '')
        if not description:
            print("  ⚠️  No description - AI analysis limited")
            self._phase6_ai = {}
            return
        
        # Build comprehensive context from all previous phases
        context = self._build_comprehensive_context()
        
        print(f"  Context: {len(context)} fields from Phases 1-5")
        
        ai_results = {}
        industry = self._phase1_basic.get('industry', '')
        
        # Business model
        print("  [AI] Analyzing business model...")
        ai_results['business_model'] = self.ai.extract_business_model_summary(description)
        
        # Moat (with financial context)
        print("  [AI] Analyzing competitive moat...")
        ai_results['moat_type'] = self.ai.categorize_moat(description, context.get('financial_metrics', {}))
        
        # Pricing power (with margin trend)
        print("  [AI] Assessing pricing power...")
        ai_results['pricing_power'] = self.ai.assess_pricing_power(description, context.get('margin_trend', 'stable'))
        
        # Complexity (with segment data)
        print("  [AI] Assessing complexity...")
        seg_count = context.get('segment_count', 0)
        geo_count = context.get('geographic_count', 0)
        ai_results['complexity_score'] = self.ai.assess_business_simplicity(description, seg_count, geo_count)
        
        # Demand type
        print("  [AI] Classifying demand type...")
        ai_results['demand_type'] = self.ai.categorize_demand_type(description, industry)
        
        self._phase6_ai = ai_results
        
        print(f"\n  ✅ Moat: {ai_results.get('moat_type', 'N/A')}")
        print(f"  ✅ Complexity: {ai_results.get('complexity_score', 'N/A')}")
        print(f"  ✅ Demand: {ai_results.get('demand_type', 'N/A')}")
    
    def _build_comprehensive_context(self) -> Dict:
        """Build complete context from all phases for AI"""
        context = {}
        
        # From Phase 1 (Yahoo Basic)
        info = self._phase1_basic.get('full_info', {})
        context['sector'] = self._phase1_basic.get('sector')
        context['industry'] = self._phase1_basic.get('industry')
        
        # From Phase 2 (Edgar)
        if self._phase2_edgar and self._phase2_edgar.get('segments'):
            segments = self._phase2_edgar['segments']
            context['segment_count'] = segments.get('segment_count', 0)
            context['segments'] = segments.get('segments', [])
        else:
            context['segment_count'] = 0
            context['segments'] = []
        
        context['geographic_count'] = 0  # Would extract from Edgar
        
        # From Phase 3 (FMP) or Phase 5 (Yahoo fallback)
        metrics = self._phase3_fmp.get('metrics_10y', {}) if self._phase3_fmp else {}
        
        # Financial metrics (prefer FMP, fallback to Yahoo, fallback to Yahoo gap-fill)
        roe_fmp = metrics.get('roe', {}).get('avg_10y')
        roe_yahoo_gap = self._phase5_yahoo_fallback.get('roe_5y_avg')
        roe_yahoo_ttm = (info.get('returnOnEquity', 0) * 100) if info.get('returnOnEquity') else 0
        
        context['financial_metrics'] = {
            'roe': roe_fmp or roe_yahoo_gap or roe_yahoo_ttm,
            'gross_margin': (info.get('grossMargins', 0) * 100) if info.get('grossMargins') else 0,
            'operating_margin': (info.get('operatingMargins', 0) * 100) if info.get('operatingMargins') else 0
        }
        
        # Margin trend
        op_margin_current = context['financial_metrics']['operating_margin']
        op_margin_5y = metrics.get('margins', {}).get('operating_avg_5y') or self._phase5_yahoo_fallback.get('operating_margin_5y')
        
        if op_margin_5y and op_margin_current:
            if op_margin_current > op_margin_5y * 1.1:
                context['margin_trend'] = 'improving'
            elif op_margin_current < op_margin_5y * 0.9:
                context['margin_trend'] = 'declining'
            else:
                context['margin_trend'] = 'stable'
        else:
            context['margin_trend'] = 'stable'
        
        return context
    
    def _compile_results(self) -> Dict:
        """Compile all data from all phases"""
        print(f"\n{'='*60}")
        print("COMPILATION COMPLETE")
        print(f"{'='*60}")
        
        result = {
            'ticker': self.ticker,
            'timestamp': datetime.now().isoformat(),
            'phase1_basic': self._phase1_basic,
            'phase2_edgar': self._phase2_edgar,
            'phase3_fmp': self._phase3_fmp,
            'phase4_fred': self._phase4_fred,
            'phase5_yahoo_fallback': self._phase5_yahoo_fallback,
            'phase6_ai': self._phase6_ai
        }
        
        # Count data sources used
        sources_used = []
        if self._phase1_basic: sources_used.append("Yahoo")
        if self._phase2_edgar: sources_used.append("Edgar")
        if self._phase3_fmp: sources_used.append("FMP")
        if self._phase4_fred: sources_used.append("FRED")
        if self._phase5_yahoo_fallback: sources_used.append("Yahoo Gap-Fill")
        if self._phase6_ai: sources_used.append("AI")
        
        print(f"\n  Sources Used: {', '.join(sources_used)}")
        print(f"  Yahoo Gaps Filled: {len(self._phase5_yahoo_fallback)}")
        print(f"\n{'='*60}\n")
        
        return result
    
    # Accessor methods for populators
    def get_basic_info(self) -> Dict:
        """Get basic company info"""
        if not self._initialized:
            self._phase1_initialize_basic()
        return self._phase1_basic
    
    def get_historical_roe_roic(self) -> Dict:
        """Get ROE/ROIC with fallback"""
        if self._phase3_fmp is None:
            return {'source': 'Not yet fetched'}
        
        metrics = self._phase3_fmp.get('metrics_10y', {})
        
        return {
            'roe_5y_avg': metrics.get('roe', {}).get('avg_5y') or self._phase5_yahoo_fallback.get('roe_5y_avg'),
            'roe_10y_avg': metrics.get('roe', {}).get('avg_10y'),
            'roic_5y_avg': metrics.get('roic', {}).get('avg_5y') or self._phase5_yahoo_fallback.get('roic_5y_avg'),
            'roic_10y_avg': metrics.get('roic', {}).get('avg_10y'),
            'source': 'FMP' if metrics.get('roe', {}).get('avg_5y') else 'Yahoo Fallback'
        }
    
    def get_ai_analysis(self) -> Dict:
        """Get AI analysis"""
        return self._phase6_ai or {}

# Test
if __name__ == "__main__":
    coordinator = DataCoordinatorV3("AAPL", "key", "key", "key")
    data = coordinator.get_all_data()
    
    print("\nFINAL DATA SUMMARY:")
    print(f"  Basic Info: {bool(data.get('phase1_basic'))}")
    print(f"  Edgar Data: {bool(data.get('phase2_edgar'))}")
    print(f"  FMP Data: {bool(data.get('phase3_fmp'))}")
    print(f"  FRED Data: {bool(data.get('phase4_fred'))}")
    print(f"  Yahoo Gaps: {len(data.get('phase5_yahoo_fallback', {}))}")
    print(f"  AI Analysis: {bool(data.get('phase6_ai'))}")
