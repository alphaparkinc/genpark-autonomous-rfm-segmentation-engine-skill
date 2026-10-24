from client import AutonomousRfmSegmentationEngineClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    engine = AutonomousRfmSegmentationEngineClient()
    print("=== AUTONOMOUS RFM SEGMENTATION ENGINE ===")
    
    profiles = [
        {"id": "USER-VIP-01", "recency": 8, "orders": 14, "spend": 3450.00},
        {"id": "USER-ATRISK-02", "recency": 120, "orders": 6, "spend": 1200.00},
        {"id": "USER-NEW-03", "recency": 5, "orders": 1, "spend": 140.00}
    ]
    
    for p in profiles:
        res = engine.segment_customer(p["id"], p["recency"], p["orders"], p["spend"])
        print()
        print(f"Customer: {res['customer_id']} | RFM: {res['rfm_scores']['composite']}")
        print(f"  Segment : {res['lifecycle_segment']}")
        print(f"  Playbook: {res['recommended_marketing_playbook']}")

if __name__ == "__main__":
    main()
