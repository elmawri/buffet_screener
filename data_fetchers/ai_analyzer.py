"""
AI Analyzer - Uses Anthropic Claude for qualitative analysis
"""
import anthropic

class AIAnalyzer:
    def __init__(self, api_key=None):
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
    
    def analyze(self, prompt, system_prompt="You are a financial analyst."):
        """Call Claude API for analysis"""
        if not self.client:
            return None
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"AI Analysis error: {e}")
            return None
