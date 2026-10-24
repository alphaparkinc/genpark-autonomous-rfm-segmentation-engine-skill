import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class AutonomousRfmSegmentationEngineClient:
    """
    Computes Recency, Frequency, Monetary (RFM) quintile boundaries (1-5)
    and maps customers to 7 canonical lifecycle segments with marketing playbooks.
    """
    def __init__(self):
        # Quintile thresholds (Recency in days, Frequency in order count, Monetary in total USD)
        self.r_bins = [15, 45, 90, 180]    # <=15 -> 5, <=45 -> 4, etc.
        self.f_bins = [1, 2, 5, 10]        # >=10 -> 5, >=5 -> 4, etc.
        self.m_bins = [100, 300, 800, 2000]# >=2000 -> 5, >=800 -> 4, etc.

    def score_recency(self, days):
        for i, bound in enumerate(self.r_bins):
            if days <= bound:
                return 5 - i
        return 1

    def score_frequency(self, orders):
        for i, bound in enumerate(reversed(self.f_bins)):
            if orders >= bound:
                return 5 - i
        return 1

    def score_monetary(self, spend):
        for i, bound in enumerate(reversed(self.m_bins)):
            if spend >= bound:
                return 5 - i
        return 1

    def classify_segment(self, r, f, m):
        if r >= 4 and f >= 4 and m >= 4:
            return "CHAMPIONS", "Exclusive VIP previews and reward loyalty bonuses"
        elif r >= 3 and f >= 3:
            return "LOYAL_CUSTOMERS", "Upsell higher value products and ask for reviews"
        elif r >= 4 and f <= 2:
            return "POTENTIAL_LOYALISTS", "Offer membership program and recommend popular add-ons"
        elif r <= 2 and f >= 4:
            return "CANT_LOSE_THEM", "Urgent win-back promotion and personal CS outreach"
        elif r <= 2 and f >= 2:
            return "AT_RISK_CUSTOMERS", "Send reactivation discount and re-engagement survey"
        elif r <= 2 and f <= 1:
            return "HIBERNATING_INACTIVE", "Re-create interest with campaign highlights or purge from list"
        else:
            return "PROMISING_ACTIVE", "Introduce onboarding tips and free shipping incentives"

    def segment_customer(self, customer_id, recency_days, total_orders, total_spend):
        r_score = self.score_recency(recency_days)
        f_score = self.score_frequency(total_orders)
        m_score = self.score_monetary(total_spend)
        
        composite_score = int(f"{r_score}{f_score}{m_score}")
        segment_name, playbook = self.classify_segment(r_score, f_score, m_score)

        return {
            "status": "success",
            "customer_id": customer_id,
            "metrics": {
                "recency_days": recency_days,
                "total_orders": total_orders,
                "total_spend": round(total_spend, 2)
            },
            "rfm_scores": {
                "recency": r_score,
                "frequency": f_score,
                "monetary": m_score,
                "composite": composite_score
            },
            "lifecycle_segment": segment_name,
            "recommended_marketing_playbook": playbook
        }
