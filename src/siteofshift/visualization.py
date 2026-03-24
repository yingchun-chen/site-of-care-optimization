import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "results"

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
    plt.savefig("results/cost_vs_asc.png")
    plt.close()

def plot_opportunity(df):
    ensure_output_dir()

    plt.figure()
    plt.scatter(df["asc_gap"], df["cost_gap"])
    plt.title("Opportunity Space: ASC Gap vs Cost Gap")
    plt.xlabel("ASC Gap (vs CBSA)")
    plt.ylabel("Cost Gap (vs CBSA)")
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