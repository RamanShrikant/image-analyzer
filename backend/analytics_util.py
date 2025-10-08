# analytics_utils.py
# Simple placeholder analytics logic to log and analyze model usage.

import datetime
import json
from collections import Counter

def record_inference(label: str, confidence: float, file_path="logs/analytics.json"):
    """Append a record of every model prediction."""
    data = {"timestamp": datetime.datetime.utcnow().isoformat(),
            "label": label,
            "confidence": confidence}
    with open(file_path, "a") as f:
        f.write(json.dumps(data) + "\n")

def summarize_inferences(file_path="logs/analytics.json"):
    """Return quick counts per label."""
    labels = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                labels.append(record["label"])
            except Exception:
                pass
    return Counter(labels)
