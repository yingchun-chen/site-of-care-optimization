from siteofshift.data import generate_data
from siteofshift.feature_engineering import (
    compute_provider_cost,
    compute_cbsa_benchmark,
    compute_gaps,
)
from siteofshift.scoring import compute_opportunity


def test_opportunity_score_created():
    df = generate_data(n=100)
    df = compute_provider_cost(df)
    df = compute_cbsa_benchmark(df)
    df = compute_gaps(df)
    df = compute_opportunity(df)

    assert "opportunity_score" in df.columns
    assert df["opportunity_score"].notna().all()