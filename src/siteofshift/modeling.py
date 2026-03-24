import yaml
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split

from siteofshift.logger import get_logger

logger = get_logger()


def train_model(df):

    # -------------------------
    # 1. Target
    # -------------------------
    df["high_cost_flag"] = (df["cost_gap"] > 0).astype(int)

    # -------------------------
    # 2. Load features
    # -------------------------
    with open("config/features.yaml", "r") as f:
        config = yaml.safe_load(f)

    features = config["features"]

    X = df[features]
    y = df["high_cost_flag"]

    # -------------------------
    # 3. Train/Test Split
    # -------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -------------------------
    # 4. Model
    # -------------------------
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        bootstrap=True,
        random_state=42
    )

    logger.info("Model initialized.")

    # -------------------------
    # 5. Fit
    # -------------------------
    model.fit(X_train, y_train)

    # -------------------------
    # 6. Feature Importance
    # -------------------------
    final_importance = pd.Series(
        model.feature_importances_,
        index=features
    )

    logger.info("Final feature importance:")
    logger.info(final_importance.to_dict())

    # -------------------------
    # 7. Predictions
    # -------------------------
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    df["high_cost_prob"] = model.predict_proba(X)[:, 1]

    # -------------------------
    # 8. Metrics
    # -------------------------
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    auc = roc_auc_score(y_test, y_prob)

    metrics_df = pd.DataFrame({
        "metric": ["sensitivity", "specificity", "auc"],
        "value": [sensitivity, specificity, auc]
    })

    metrics_df.to_csv("results/model_metrics.csv", index=False)

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig("results/roc_curve.png")
    plt.close()

    return model, df