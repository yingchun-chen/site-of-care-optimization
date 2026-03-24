import pandas as pd
import numpy as np

def generate_data(n=5000):
    np.random.seed(42)

    df = pd.DataFrame({
        "provider_id": np.arange(n),
        "cbsa": np.random.choice(["NY", "CA", "TX", "FL"], n),
        "procedure_volume": np.random.randint(20, 200, n),
        "risk_score": np.random.normal(1.0, 0.3, n)
    })

    # Site-of-care distribution
    asc = np.random.uniform(0.2, 0.7, n)
    hopd = np.random.uniform(0.2, 0.6, n)
    inpatient = np.random.uniform(0.05, 0.2, n)

    total = asc + hopd + inpatient

    df["asc_rate"] = asc / total
    df["hopd_rate"] = hopd / total
    df["inpatient_rate"] = inpatient / total

    # Cost by site
    df["asc_cost"] = np.random.normal(15000, 2000, n)
    df["hopd_cost"] = np.random.normal(25000, 3000, n)
    df["inpatient_cost"] = np.random.normal(35000, 5000, n)

    return df