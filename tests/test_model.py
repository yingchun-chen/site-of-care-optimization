from siteofshift.data import generate_data
from siteofshift.feature_engineering import (
    compute_provider_cost,
    compute_cbsa_benchmark,
    compute_gaps,
)
from siteofshift.scoring import compute_opportunity
from siteofshift.modeling import train_model


def test_model_runs():
    df = generate_data(n=200)
    df = compute_provider_cost(df)
    df = compute_cbsa_benchmark(df)
    df = compute_gaps(df)
    df = compute_opportunity(df)

    model, df = train_model(df)

    assert model is not None
    assert "high_cost_prob" in df.columns
    assert df["high_cost_prob"].notna().all()