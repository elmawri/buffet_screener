"""
Buffett Screener - Automatic Scoring Engine
Calculates 1-10 scores for each criterion based on quantitative metrics
"""

class BuffettScorer:
    """Automatic scoring algorithms for all Buffett criteria"""
    
    @staticmethod
    def calculate_simplicity_score(data):
        """
        Calculate simplicity score (1-10)
        Higher = Simpler business
        """
        score = 10  # Start perfect
        
        # Segment complexity penalty
        segment_count = data.get('segment_count', 0)
        if segment_count > 5:
            score -= 2
        elif segment_count > 3:
            score -= 1
        
        # Geographic complexity penalty
        geo_count = data.get('geo_count', 0)
        if geo_count > 15:
            score -= 2
        elif geo_count > 8:
            score -= 1
        
        # Derivatives/complex instruments
        if data.get('has_derivatives', False):
            score -= 2
        
        # Banking/Insurance (inherently complex)
        if data.get('is_financial', False):
            score -= 2
        
        # AI complexity assessment (1-10, where 10 = very complex)
        ai_complexity = data.get('ai_complexity_score', 5)
        if ai_complexity >= 8:
            score -= 3
        elif ai_complexity >= 6:
            score -= 2
        elif ai_complexity >= 4:
            score -= 1
        
        # Product complexity
        if data.get('products') == 'Many':
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_operating_history_score(data):
        """
        Calculate operating history score (1-10)
        Higher = Longer, more consistent history
        """
        score = 5  # Start neutral
        
        # Longevity bonus
        years_public = data.get('years_listed', 0)
        if years_public >= 50:
            score += 3
        elif years_public >= 30:
            score += 2
        elif years_public >= 15:
            score += 1
        elif years_public < 5:
            score -= 2
        
        # Revenue consistency (CoV = Coefficient of Variation)
        revenue_cov = data.get('revenue_cov', 15)  # Default moderate
        if revenue_cov < 5:
            score += 2
        elif revenue_cov < 10:
            score += 1
        elif revenue_cov > 30:
            score -= 2
        
        # Earnings consistency
        earnings_cov = data.get('earnings_cov', 20)
        if earnings_cov < 10:
            score += 2
        elif earnings_cov < 20:
            score += 1
        elif earnings_cov > 50:
            score -= 2
        
        # No restatements = good
        if not data.get('has_restatements', False):
            score += 1
        else:
            score -= 2
        
        # Strategy stability
        if not data.get('major_pivots', False):
            score += 1
        else:
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_moat_score(data):
        """
        Calculate moat score (1-10)
        Higher = Stronger competitive advantage
        """
        score = 3  # Start low (moats are rare)
        
        # Moat type strength
        moat_type = data.get('moat_type', 'None')
        if moat_type in ['Brand', 'Network Effects']:
            score += 3
        elif moat_type in ['Regulatory/Licenses', 'Switching Costs']:
            score += 2
        elif moat_type == 'Cost Advantage':
            score += 2
        
        # Pricing power evidence
        pricing = data.get('pricing_power', 'No')
        if pricing == 'Yes':
            score += 3
        elif pricing == 'Moderate':
            score += 1
        
        # ROIC evidence (Buffett: ROIC > 15% suggests moat)
        roic_avg = data.get('roic_5y_avg', 0)
        if roic_avg > 25:
            score += 2
        elif roic_avg > 20:
            score += 1.5
        elif roic_avg > 15:
            score += 1
        elif roic_avg < 10 and roic_avg > 0:
            score -= 1
        
        # Margin sustainability
        gross_margin = data.get('gross_margin_5y_avg', 0)
        if gross_margin > 60:
            score += 1
        
        # Margin trend
        margin_trend = data.get('margin_trend', 'stable')
        if margin_trend == 'improving':
            score += 0.5
        elif margin_trend == 'declining':
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_management_score(data):
        """
        Calculate management score (1-10)
        Higher = Better aligned, better capital allocation
        """
        score = 5  # Start neutral
        
        # Insider ownership (skin in the game)
        insider_pct = data.get('insider_ownership_pct', 0)
        if insider_pct > 20:
            score += 2
        elif insider_pct > 10:
            score += 1
        elif insider_pct < 1:
            score -= 1
        
        # CEO tenure (experience vs entrenchment)
        ceo_tenure = data.get('ceo_tenure_years', 0)
        if 5 <= ceo_tenure <= 20:
            score += 1
        elif ceo_tenure > 30:
            score -= 0.5
        elif ceo_tenure < 2:
            score -= 0.5
        
        # Share buybacks timing
        shares_change = data.get('shares_5y_change_pct', 0)
        avg_pe = data.get('avg_pe_ratio', 20)
        
        if shares_change < -15:  # Significant buybacks
            if avg_pe < 15:
                score += 3
            elif avg_pe < 20:
                score += 2
        elif shares_change > 10:  # Diluting
            score -= 2
        
        # Compensation alignment
        if data.get('compensation_aligned', False):
            score += 1
        
        # Dividend sustainability
        payout_ratio = data.get('dividend_payout_ratio', 50)
        if 30 <= payout_ratio <= 60:
            score += 1
        elif payout_ratio > 90:
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_roe_roic_score(data):
        """
        Calculate ROE/ROIC score (1-10)
        Higher = Better returns on capital
        """
        score = 0
        
        # ROE scoring
        roe_avg = data.get('roe_5y_avg', 0)
        if roe_avg > 25:
            score += 4
        elif roe_avg > 20:
            score += 3
        elif roe_avg > 15:
            score += 2
        elif roe_avg > 10:
            score += 1
        
        # ROIC scoring (more important)
        roic_avg = data.get('roic_5y_avg', 0)
        if roic_avg > 20:
            score += 4
        elif roic_avg > 15:
            score += 3
        elif roic_avg > 12:
            score += 2
        elif roic_avg > 10:
            score += 1
        
        # Consistency bonus
        roe_std = data.get('roe_std_dev', 5)
        if roe_std < 3:
            score += 1
        
        # Penalty for excessive leverage
        roe_roic_diff = roe_avg - roic_avg
        debt_to_equity = data.get('debt_to_equity', 0.5)
        if roe_roic_diff > 10 and debt_to_equity > 1:
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_predictability_score(data):
        """
        Calculate predictability score (1-10)
        Higher = More predictable earnings/revenue
        """
        score = 5  # Start neutral
        
        # Revenue predictability
        revenue_cov = data.get('revenue_cov', 15)
        if revenue_cov < 3:
            score += 3
        elif revenue_cov < 5:
            score += 2
        elif revenue_cov < 10:
            score += 1
        elif revenue_cov > 25:
            score -= 2
        
        # Earnings predictability
        earnings_cov = data.get('earnings_cov', 20)
        if earnings_cov < 5:
            score += 3
        elif earnings_cov < 10:
            score += 2
        elif earnings_cov < 20:
            score += 1
        elif earnings_cov > 50:
            score -= 2
        
        # Margin stability
        margin_std = data.get('margin_std_dev', 3)
        if margin_std < 2:
            score += 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_capital_allocation_score(data):
        """
        Calculate capital allocation score (1-10)
        Higher = Better use of capital
        """
        score = 5  # Start neutral
        
        # Share buybacks (when smart)
        shares_change = data.get('shares_5y_change_pct', 0)
        avg_pe = data.get('avg_pe_during_buyback', 20)
        
        if shares_change < -15:  # Significant buybacks
            if avg_pe < 15:
                score += 3
            elif avg_pe < 20:
                score += 2
        elif shares_change > 10:
            score -= 2
        
        # Dividend sustainability
        payout_ratio = data.get('dividend_payout_ratio', 50)
        dividend_growth = data.get('dividend_5y_cagr', 0)
        
        if 30 <= payout_ratio <= 60 and dividend_growth > 0:
            score += 2
        elif payout_ratio > 90:
            score -= 2
        
        # Reinvestment discipline
        reinvest_rate = data.get('reinvestment_rate', 50)
        roic = data.get('roic_avg', 10)
        
        if roic > 15 and reinvest_rate > 50:
            score += 2
        elif roic < 10 and reinvest_rate > 70:
            score -= 1
        
        # M&A discipline
        if data.get('has_ma', False):
            roic_post = data.get('roic_post_ma', 10)
            roic_pre = data.get('roic_pre_ma', 10)
            if roic_post >= roic_pre:
                score += 2
            else:
                score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_leverage_score(data):
        """
        Calculate leverage score (1-10)
        Higher = Lower leverage, safer
        """
        score = 10  # Start perfect
        
        # Net Debt / EBITDA
        net_debt_ebitda = data.get('net_debt_ebitda', 2)
        if net_debt_ebitda < 0:  # Net cash
            score = 10
        elif net_debt_ebitda < 1:
            score -= 0
        elif net_debt_ebitda < 2:
            score -= 1
        elif net_debt_ebitda < 3:
            score -= 3
        elif net_debt_ebitda < 4:
            score -= 5
        else:
            score -= 7
        
        # Interest Coverage
        interest_coverage = data.get('interest_coverage', 5)
        if interest_coverage < 3:
            score -= 3
        elif interest_coverage < 5:
            score -= 1
        
        # Debt maturity
        short_term_pct = data.get('short_term_debt_pct', 30)
        if short_term_pct > 50:
            score -= 2
        
        # Debt trend
        debt_growth = data.get('debt_5y_cagr', 0)
        fcf_growth = data.get('fcf_5y_cagr', 0)
        if debt_growth > fcf_growth:
            score -= 1
        
        return max(1, min(10, round(score, 1)))
    
    @staticmethod
    def calculate_resilience_score(data):
        """
        Calculate resilience score (1-10)
        Higher = More resilient in crises
        """
        score = 5  # Start neutral
        
        # 2008-09 GFC performance
        revenue_2008 = data.get('revenue_change_2008', 0)
        if revenue_2008 > 0:
            score += 3
        elif revenue_2008 > -10:
            score += 2
        elif revenue_2008 > -20:
            score += 1
        elif revenue_2008 < -30:
            score -= 2
        
        # 2020 COVID performance
        revenue_2020 = data.get('revenue_change_2020', 0)
        if revenue_2020 > 0:
            score += 2
        elif revenue_2020 > -10:
            score += 1
        elif revenue_2020 < -30:
            score -= 1
        
        # Dividend reliability
        if not data.get('dividend_cuts', False):
            score += 2
        else:
            score -= 2
        
        # Demand type
        demand = data.get('demand_type', 'Mixed')
        if demand == 'Recurring':
            score += 2
        elif demand == 'Discretionary':
            score -= 1
        
        # Risk factors
        if data.get('customer_diversification') == 'High':
            score += 1
        elif data.get('customer_diversification') == 'Low':
            score -= 1
        
        return max(1, min(10, round(score, 1)))
