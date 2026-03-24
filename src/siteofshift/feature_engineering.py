def compute_provider_cost(df):
    df["provider_avg_cost"] = (
        df["asc_rate"] * df["asc_cost"] +
        df["hopd_rate"] * df["hopd_cost"] +
        df["inpatient_rate"] * df["inpatient_cost"]
    )
    return df


def compute_cbsa_benchmark(df):
    df["cbsa_asc_avg"] = df.groupby("cbsa")["asc_rate"].transform("mean")
    df["cbsa_cost_avg"] = df.groupby("cbsa")["provider_avg_cost"].transform("mean")
    return df


def compute_gaps(df):
    df["asc_gap"] = df["cbsa_asc_avg"] - df["asc_rate"]
    df["cost_gap"] = df["provider_avg_cost"] - df["cbsa_cost_avg"]
    return df