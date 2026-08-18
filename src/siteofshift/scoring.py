def compute_opportunity(df):
    df = df.copy()

    # ASC shortfall:
    # Positive only when provider ASC use is below the CBSA benchmark.
    #
    # asc_gap = provider ASC rate - CBSA ASC rate
    # Therefore:
    # asc_gap < 0 means provider ASC utilization is below benchmark.
    df["asc_shortfall"] = (
        -df["asc_gap"]
    ).clip(lower=0)

    # Excess cost:
    # Positive only when provider average cost is above
    # the CBSA benchmark.
    #
    # cost_gap = provider_avg_cost - cbsa_cost_avg
    # Therefore:
    # cost_gap > 0 means provider cost is above benchmark.
    df["excess_cost"] = (
        df["cost_gap"]
    ).clip(lower=0)

    # Opportunity score:
    # Higher volume × larger ASC shortfall × higher excess cost
    # = larger potential site-of-service opportunity.
    df["opportunity_score"] = (
        df["procedure_volume"]
        * df["asc_shortfall"]
        * df["excess_cost"]
    )

    return df