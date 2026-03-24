import yaml
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings

warnings.filterwarnings("ignore")


def run_uplift_model(df):
    """
    T-Learner implementation for uplift modeling
    """

    # -----------------------------
    # 1. Treatment assignment
    # -----------------------------
    df["treatment"] = np.random.choice(
        ["control", "treatment"], size=len(df)
    )

    treatment_flag = (df["treatment"] == "treatment").astype(int)

    # -----------------------------
    # 2. Simulate heterogeneous treatment effect
    # -----------------------------
    noise = np.random.normal(0, 0.01, len(df))

    true_effect = (
        0.15 * df["asc_gap"] +
        0.10 * (df["procedure_volume"] / df["procedure_volume"].max()) -
        0.08 * df["risk_score"]
    )

    df["asc_rate_post"] = df["asc_rate"] + treatment_flag * (true_effect + noise)

    # -----------------------------
    # 3. Feature Engineering
    # -----------------------------
    df["volume_x_gap"] = df["procedure_volume"] * df["asc_gap"]
    df["cost_x_gap"] = df["cost_gap"] * df["asc_gap"]

    # -------------------------
    # 2. Load features
    # -------------------------
    features = [
        "procedure_volume",
        "asc_rate",
        "cost_gap",
        "risk_score",
        "volume_x_gap",
        "cost_x_gap"
    ]

    X = df[features]

    # -----------------------------
    # 4. Train T-Learner models
    # -----------------------------
    treated = df["treatment"] == "treatment"
    control = df["treatment"] == "control"

    model_t = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model_c = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model_t.fit(X[treated], df.loc[treated, "asc_rate_post"])
    model_c.fit(X[control], df.loc[control, "asc_rate_post"])

    # -----------------------------
    # 5. Predict uplift
    # -----------------------------
    mu1 = model_t.predict(X)  # treated outcome
    mu0 = model_c.predict(X)  # control outcome

    df["uplift_score"] = mu1 - mu0

    # -----------------------------
    # 6. Feature importance
    # -----------------------------
    feature_importance = pd.Series(
        model_t.feature_importances_,
        index=features
    ).sort_values(ascending=False)

    print("\nUplift Feature Importance:")
    print(feature_importance)

    # -----------------------------
    # 7. Debug checks
    # -----------------------------
    print("\nUplift Score Summary:")
    print(df["uplift_score"].describe())
    print("Unique values:", df["uplift_score"].nunique())

    # -----------------------------
    # 8. Segmentation
    # -----------------------------
    try:
        df["uplift_segment"] = pd.qcut(
            df["uplift_score"],
            q=3,
            labels=["Low", "Medium", "High"]
        )
    except ValueError:
        # fallback if distribution is weird
        df["uplift_segment"] = pd.cut(
            df["uplift_score"],
            bins=2,
            labels=["Low", "High"]
        )

    segment_summary = df.groupby("uplift_segment")[features].mean()

    print("\nUplift Segment Summary:")
    print(segment_summary)

    return df, feature_importance