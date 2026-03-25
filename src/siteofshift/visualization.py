import matplotlib.pyplot as plt
import os
import yaml
OUTPUT_DIR = "results"

def load_ui_config():
    with open("config/ui.yaml", "r") as f:
        return yaml.safe_load(f)

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def plot_site_of_care(df):
    ensure_output_dir()

    plt.figure()
    plt.hist(df["asc_rate"], bins=20)
    plt.title("ASC Rate Across Providers")
    plt.xlabel("ASC Rate")
    plt.ylabel("Number of Providers")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/asc_distribution.png")
    plt.close()

def plot_cost_vs_asc(df):
    ensure_output_dir()
    
    plt.figure()
    plt.scatter(df["asc_rate"], df["provider_avg_cost"])
    plt.xlabel("ASC Rate")
    plt.ylabel("Provider Average Cost")
    plt.title("ASC Rate vs Avg. Cost")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/cost_vs_asc.png")
    plt.close()

def plot_opportunity(df):
    ensure_output_dir()

    plot_df = df.copy()

    # dominant site of service
    site_cols = ["asc_rate", "hopd_rate", "inpatient_rate"]
    plot_df["dominant_site"] = plot_df[site_cols].idxmax(axis=1)
    plot_df["dominant_site"] = plot_df["dominant_site"].replace({
        "asc_rate": "ASC",
        "hopd_rate": "HOPD",
        "inpatient_rate": "Inpatient"

    })

    fig, ax = plt.subplots()

    for site in ["ASC", "HOPD", "Inpatient"]:
        site_df = plot_df[plot_df["dominant_site"] == site]
        ax.scatter(site_df["asc_gap"], site_df["cost_gap"], label=site, alpha=0.7)

    ax.set_title("Opportunity Space: ASC Gap vs Cost Gap by Dominant Site of Service")

    ax.set_xlabel("ASC Gap (vs CBSA)")
    ax.set_ylabel("Cost Gap (vs CBSA)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/opportunity_scatter.png")
    plt.close()


def plot_uplift(df):
    ensure_output_dir()

    plt.figure()
    plt.hist(df["uplift_score"], bins=20)
    plt.title("Distribution of Uplift Scores")
    plt.xlabel("Uplift Score")
    plt.ylabel("Number of Providers")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/uplift_distribution.png")
    plt.close()

    
def plot_uplift_feature_importance(feature_importance):
    ensure_output_dir()

    plt.figure()
    feature_importance.plot(kind="bar")
    plt.title("Uplift Model Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/uplift_feature_importance.png")
    plt.close()


def plot_uplift_segments(df):
    ensure_output_dir()

    segment_means = df.groupby("uplift_segment")[
        ["asc_rate", "cost_gap", "procedure_volume", "risk_score"]
    ].mean()

    segment_means.plot(kind="bar")
    plt.title("Feature Averages by Uplift Segment")
    plt.xlabel("Uplift Segment")
    plt.ylabel("Average Value")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/uplift_segments.png")
    plt.close()