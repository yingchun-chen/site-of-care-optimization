import os
from siteofshift.data import generate_data
from siteofshift.feature_engineering import (
    compute_provider_cost,
    compute_cbsa_benchmark,
    compute_gaps
)
from siteofshift.scoring import compute_opportunity
from siteofshift.modeling import train_model
from siteofshift.uplift import run_uplift_model
from siteofshift.logger import get_logger

from siteofshift.visualization import (
    plot_site_of_care,
    plot_opportunity,
    plot_uplift,
    plot_uplift_feature_importance,
    plot_uplift_segments
)

logger = get_logger()

def main():
    os.makedirs("results", exist_ok=True)
    logger.info("Starting Site-of-Care Optimization pipeline...")

    df = generate_data()

    df = compute_provider_cost(df)
    df = compute_cbsa_benchmark(df)
    df = compute_gaps(df)
    df = compute_opportunity(df)

    model, df = train_model(df)

    df, feature_importance = run_uplift_model(df)

    df["final_score"] = (
        df["opportunity_score"] * df["uplift_score"]
    )

    logger.info("Top providers by opportunity score:")
    print(df.sort_values("opportunity_score", ascending=False).head())

    logger.info("Top providers by uplift score:")
    print(df.sort_values("uplift_score", ascending=False).head())

    # Visualizations
    plot_uplift_feature_importance(feature_importance)
    plot_uplift_segments(df)
    plot_site_of_care(df)
    plot_opportunity(df)
    plot_uplift(df)
    df.to_csv("results/final_output.csv", index=False)

if __name__ == "__main__":
    main()
