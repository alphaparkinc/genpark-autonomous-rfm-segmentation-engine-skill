import sys, json
from client import AutonomousRfmSegmentationEngineClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    engine = AutonomousRfmSegmentationEngineClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-autonomous-rfm-segmentation-engine-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    cid = req.get("customer_id", "CUST_001")
    r = int(req.get("recency_days", 30))
    f = int(req.get("total_orders", 3))
    m = float(req.get("total_spend", 250.0))
    res = engine.segment_customer(cid, r, f, m)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
