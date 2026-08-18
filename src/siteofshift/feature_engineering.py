def validate_site_rates(df, tolerance=1e-6):
    """
    Validate that ASC, HOPD, and inpatient rates sum to 1
    for each provider.
    """
    df = df.copy()

    df["site_rate_sum"] = (
        df["asc_rate"]
        + df["hopd_rate"]
        + df["inpatient_rate"]
    )

    invalid = df[
        (df["site_rate_sum"] - 1.0).abs() > tolerance
    ]

    if not invalid.empty:
        raise ValueError(
            f"{len(invalid)} rows have site-of-care rates "
            f"that do not sum to 1."
        )

    return df


def compute_provider_cost(df):
    df = df.copy()

    df["n_asc"] = df["procedure_volume"] * df["asc_rate"]
    df["n_hopd"] = df["procedure_volume"] * df["hopd_rate"]
    df["n_inpatient"] = (
        df["procedure_volume"] * df["inpatient_rate"]
    )

    df["provider_cost_in_total_asc"] = (
        df["n_asc"] * df["asc_cost"]
    )

    df["provider_cost_in_total_hopd"] = (
        df["n_hopd"] * df["hopd_cost"]
    )

    df["provider_cost_in_total_inpatient"] = (
        df["n_inpatient"] * df["inpatient_cost"]
    )

    df["provider_cost_in_total"] = (
        df["provider_cost_in_total_asc"]
        + df["provider_cost_in_total_hopd"]
        + df["provider_cost_in_total_inpatient"]
    )

    df["provider_avg_cost"] = (
        df["provider_cost_in_total"]
        / df["procedure_volume"]
    )

    return df


def compute_cbsa_benchmark(df):
    df = df.copy()

    df["cbsa_total_volume"] = (
        df.groupby("cbsa")["procedure_volume"]
        .transform("sum")
    )

    df["cbsa_total_asc_volume"] = (
        df.groupby("cbsa")["n_asc"]
        .transform("sum")
    )

    df["cbsa_total_cost"] = (
        df.groupby("cbsa")["provider_cost_in_total"]
        .transform("sum")
    )

    df["cbsa_asc_avg"] = (
        df["cbsa_total_asc_volume"]
        / df["cbsa_total_volume"]
    )

    df["cbsa_cost_avg"] = (
        df["cbsa_total_cost"]
        / df["cbsa_total_volume"]
    )

    return df


def compute_gaps(df):
    df = df.copy()

    df["asc_gap"] = (
        df["asc_rate"] - df["cbsa_asc_avg"]
    )

    df["cost_gap"] = (
        df["provider_avg_cost"] - df["cbsa_cost_avg"]
    )
    return df
