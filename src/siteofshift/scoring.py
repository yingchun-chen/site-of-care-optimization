def compute_opportunity(df):
    df["opportunity_score"] = (
        df["asc_gap"] *
        df["procedure_volume"] *
        df["cost_gap"]
    )
    return df