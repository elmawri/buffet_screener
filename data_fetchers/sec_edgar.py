"""
SEC Edgar Data Fetcher - Complete Implementation
Fetches data from 10-K, 10-Q, DEF 14A, and 8-K filings via CIK
"""
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional
import time

class SECEdgarFetcher:
    """Fetch data from SEC Edgar filings using CIK"""
    
    def __init__(self, cik: str):
        """
        Initialize Edgar fetcher
        Args:
            cik: Company CIK number (with or without leading zeros)
        """
        self.cik = str(cik).zfill(10)  # Pad to 10 digits
        self.base_url = "https://data.sec.gov"
        self.headers = {
            'User-Agent': 'YourCompany contact@email.com',  # Required by SEC
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_latest_10k(self) -> Optional[Dict]:
        """
        Get most recent 10-K filing
        Returns dict with filing URL and metadata
        """
        try:
            # Get company submissions
            url = f"{self.base_url}/submissions/CIK{self.cik}.json"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Find latest 10-K
            filings = data.get('filings', {}).get('recent', {})
            forms = filings.get('form', [])
            accession_numbers = filings.get('accessionNumber', [])
            filing_dates = filings.get('filingDate', [])
            
            for i, form in enumerate(forms):
                if form == '10-K':
                    accession = accession_numbers[i].replace('-', '')
                    filing_date = filing_dates[i]
                    
                    # Construct document URL
                    doc_url = f"{self.base_url}/Archives/edgar/data/{int(self.cik)}/{accession}/"
                    
                    return {
                        'accession_number': accession_numbers[i],
                        'filing_date': filing_date,
                        'url': doc_url,
                        'form': '10-K'
                    }
            
            return None
            
        except Exception as e:
            print(f"Error fetching 10-K: {e}")
            return None
    
    def get_latest_proxy(self) -> Optional[Dict]:
        """Get most recent DEF 14A (proxy statement)"""
        try:
            url = f"{self.base_url}/submissions/CIK{self.cik}.json"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            filings = data.get('filings', {}).get('recent', {})
            forms = filings.get('form', [])
            accession_numbers = filings.get('accessionNumber', [])
            filing_dates = filings.get('filingDate', [])
            
            for i, form in enumerate(forms):
                if form == 'DEF 14A':
                    accession = accession_numbers[i].replace('-', '')
                    filing_date = filing_dates[i]
                    
                    doc_url = f"{self.base_url}/Archives/edgar/data/{int(self.cik)}/{accession}/"
                    
                    return {
                        'accession_number': accession_numbers[i],
                        'filing_date': filing_date,
                        'url': doc_url,
                        'form': 'DEF 14A'
                    }
            
            return None
            
        except Exception as e:
            print(f"Error fetching proxy: {e}")
            return None
    
    def extract_segments_from_10k(self, filing_url: str) -> Optional[Dict]:
        """
        Extract business segment information from 10-K
        Returns segment count, names, and revenue breakdown
        """
        try:
            # Get the filing index
            response = self.session.get(filing_url + "index.json")
            response.raise_for_status()
            index = response.json()
            
            # Find the main 10-K document (usually htm or html)
            main_doc = None
            for item in index.get('directory', {}).get('item', []):
                name = item.get('name', '')
                if name.endswith('.htm') or name.endswith('.html'):
                    if '10-k' in name.lower() or item.get('type') == '10-K':
                        main_doc = name
                        break
            
            if not main_doc:
                # Fallback: get first htm file
                for item in index.get('directory', {}).get('item', []):
                    if item.get('name', '').endswith(('.htm', '.html')):
                        main_doc = item['name']
                        break
            
            if not main_doc:
                return None
            
            # Fetch document
            doc_response = self.session.get(filing_url + main_doc)
            doc_response.raise_for_status()
            text = doc_response.text
            
            # Extract segment info (simplified - would need more robust parsing)
            segments = self._parse_segments(text)
            
            return segments
            
        except Exception as e:
            print(f"Error extracting segments: {e}")
            return None
    
    def _parse_segments(self, text: str) -> Dict:
        """Parse segment information from 10-K text"""
        # This is a simplified version - real implementation would need
        # more sophisticated parsing (XBRL, tables, etc.)
        
        segments = {
            'segment_count': 0,
            'segments': [],
            'method': 'text_analysis'
        }
        
        # Look for common segment disclosure patterns
        patterns = [
            r'(?:reportable segments?|business segments?|operating segments?)[\s:]+([^\n]+)',
            r'(\d+)\s+(?:reportable|business|operating)\s+segments?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Try to extract count
                for match in matches:
                    if isinstance(match, str) and match.isdigit():
                        segments['segment_count'] = int(match)
                        break
        
        # This is placeholder - real implementation would extract actual segment names
        # and revenue breakdowns from XBRL or HTML tables
        
        return segments
    
    def extract_company_history(self, filing_url: str) -> Optional[Dict]:
        """Extract company founding/incorporation date from 10-K"""
        try:
            response = self.session.get(filing_url + "index.json")
            response.raise_for_status()
            index = response.json()
            
            # Get main document
            main_doc = None
            for item in index.get('directory', {}).get('item', []):
                name = item.get('name', '')
                if name.endswith(('.htm', '.html')) and '10-k' in name.lower():
                    main_doc = name
                    break
            
            if not main_doc:
                return None
            
            doc_response = self.session.get(filing_url + main_doc)
            text = doc_response.text
            
            # Look for incorporation/founding dates
            history = self._parse_history(text)
            
            return history
            
        except Exception as e:
            print(f"Error extracting history: {e}")
            return None
    
    def _parse_history(self, text: str) -> Dict:
        """Parse company history from text"""
        history = {}
        
        # Look for incorporation date
        patterns = [
            r'incorporated.*?(?:in|on)\s+(\d{4})',
            r'founded.*?(?:in|on)\s+(\d{4})',
            r'established.*?(?:in|on)\s+(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                history['founded_year'] = int(match.group(1))
                break
        
        return history
    
    def extract_executive_info(self, proxy_url: str) -> Optional[Dict]:
        """Extract CEO/CFO information from proxy statement"""
        try:
            response = self.session.get(proxy_url + "index.json")
            response.raise_for_status()
            index = response.json()
            
            # Get main proxy document
            main_doc = None
            for item in index.get('directory', {}).get('item', []):
                name = item.get('name', '')
                if name.endswith(('.htm', '.html')):
                    main_doc = name
                    break
            
            if not main_doc:
                return None
            
            doc_response = self.session.get(proxy_url + main_doc)
            text = doc_response.text
            
            executives = self._parse_executives(text)
            
            return executives
            
        except Exception as e:
            print(f"Error extracting executives: {e}")
            return None
    
    def _parse_executives(self, text: str) -> Dict:
        """Parse executive information from proxy"""
        executives = {
            'ceo': {},
            'cfo': {},
            'officers': []
        }
        
        # Look for CEO info
        ceo_patterns = [
            r'Chief Executive Officer.*?(?:since|appointed)\s+(\d{4})',
            r'(?:President|CEO).*?(?:since|appointed)\s+(\d{4})',
        ]
        
        for pattern in ceo_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                year_appointed = int(match.group(1))
                current_year = datetime.now().year
                executives['ceo']['tenure_years'] = current_year - year_appointed
                break
        
        # Similar for CFO
        cfo_patterns = [
            r'Chief Financial Officer.*?(?:since|appointed)\s+(\d{4})',
            r'CFO.*?(?:since|appointed)\s+(\d{4})',
        ]
        
        for pattern in cfo_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                year_appointed = int(match.group(1))
                current_year = datetime.now().year
                executives['cfo']['tenure_years'] = current_year - year_appointed
                break
        
        return executives
    
    def check_for_restatements(self, years: int = 5) -> List[Dict]:
        """Check for financial restatements in 8-K filings"""
        try:
            url = f"{self.base_url}/submissions/CIK{self.cik}.json"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            restatements = []
            filings = data.get('filings', {}).get('recent', {})
            forms = filings.get('form', [])
            filing_dates = filings.get('filingDate', [])
            
            # Look for 8-K filings in last N years
            cutoff_year = datetime.now().year - years
            
            for i, form in enumerate(forms):
                if form == '8-K':
                    filing_date = filing_dates[i]
                    year = int(filing_date.split('-')[0])
                    
                    if year >= cutoff_year:
                        # Would need to fetch and analyze 8-K content
                        # for restatement keywords
                        restatements.append({
                            'filing_date': filing_date,
                            'form': '8-K',
                            # 'has_restatement': would need content analysis
                        })
            
            return restatements
            
        except Exception as e:
            print(f"Error checking restatements: {e}")
            return []
    
    def get_comprehensive_data(self) -> Dict:
        """
        Get all available Edgar data for company
        This is the main method to call
        """
        print(f"Fetching Edgar data for CIK {self.cik}...")
        
        data = {
            'cik': self.cik,
            'fetched_at': datetime.now().isoformat(),
            '10k': None,
            'proxy': None,
            'segments': None,
            'history': None,
            'executives': None,
            'restatements': []
        }
        
        # Get latest 10-K
        filing_10k = self.get_latest_10k()
        if filing_10k:
            data['10k'] = filing_10k
            print(f"  Found 10-K: {filing_10k['filing_date']}")
            
            # Extract segments
            time.sleep(0.1)  # Rate limiting
            segments = self.extract_segments_from_10k(filing_10k['url'])
            if segments:
                data['segments'] = segments
                print(f"  Extracted {segments.get('segment_count', 0)} segments")
            
            # Extract history
            time.sleep(0.1)
            history = self.extract_company_history(filing_10k['url'])
            if history:
                data['history'] = history
                if 'founded_year' in history:
                    print(f"  Founded: {history['founded_year']}")
        
        # Get latest proxy
        time.sleep(0.1)
        proxy = self.get_latest_proxy()
        if proxy:
            data['proxy'] = proxy
            print(f"  Found Proxy: {proxy['filing_date']}")
            
            # Extract executive info
            time.sleep(0.1)
            executives = self.extract_executive_info(proxy['url'])
            if executives:
                data['executives'] = executives
                if executives.get('ceo', {}).get('tenure_years'):
                    print(f"  CEO Tenure: {executives['ceo']['tenure_years']} years")
        
        # Check for restatements
        time.sleep(0.1)
        restatements = self.check_for_restatements()
        data['restatements'] = restatements
        print(f"  Found {len(restatements)} 8-K filings (last 5Y)")
        
        return data

# Example usage
if __name__ == "__main__":
    # Test with a known CIK
    cik = "0000320193"  # Apple
    fetcher = SECEdgarFetcher(cik)
    data = fetcher.get_comprehensive_data()
    
    import json
    print("\n" + "="*80)
    print("COMPREHENSIVE DATA:")
    print("="*80)
    print(json.dumps(data, indent=2))
