import numpy as np
import pandas as pd


def create_sample_dataset(n=400, seed=42):
    """Create reproducible synthetic student-service request records."""
    rng = np.random.default_rng(seed)
    request_types = np.array(["Enrollment", "Document Request", "Technical Support", "Scholarship", "Payment"])
    priorities = np.array(["Low", "Normal", "High", "Urgent"])
    channels = np.array(["Online Form", "Email", "Walk-in"])
    req_type = rng.choice(request_types, n, p=[.28, .25, .20, .12, .15])
    priority = rng.choice(priorities, n, p=[.25, .40, .25, .10])
    channel = rng.choice(channels, n, p=[.60, .20, .20])
    days_open = rng.integers(0, 16, n)
    workload = rng.integers(1, 21, n)
    satisfaction = rng.integers(1, 6, n)
    priority_effect = pd.Series(priority).map({"Low": 0, "Normal": 1, "High": 2, "Urgent": 3}).to_numpy()
    probability = 1 / (1 + np.exp(-(-3.0 + .25 * days_open + .09 * workload + .45 * priority_effect)))
    breached = rng.binomial(1, probability)
    dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 300, n), unit="D")
    return pd.DataFrame({
        "Request_ID": [f"SR-{i:04d}" for i in range(1, n + 1)],
        "Request_Date": dates,
        "Request_Type": req_type,
        "Priority": priority,
        "Submission_Channel": channel,
        "Days_Open": days_open,
        "Staff_Workload": workload,
        "Satisfaction_Score": satisfaction,
        "SLA_Breached": breached,
    })
