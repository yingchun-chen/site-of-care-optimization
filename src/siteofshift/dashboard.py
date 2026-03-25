import yaml
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# plot Uplift Gain Curve
def plot_uplift_gain_curve(df):
    df_sorted = df.sort_values("uplift_score", ascending=False).reset_index(drop=True)

    df_sorted["cumulative_uplift_gain"] = df_sorted["uplift_score"].cumsum()
    df_sorted["population_pct"] = (df_sorted.index + 1) / len(df_sorted)

    # random baseline
    total_gain = df_sorted["uplift_score"].sum()
    df_sorted["random_baseline"] = df_sorted["population_pct"] * total_gain

    fig, ax = plt.subplots()

    ax.plot(
        df_sorted["population_pct"],
        df_sorted["cumulative_uplift_gain"],
        label="Model Ranking",
        linewidth=2
    )
    ax.plot(
        df_sorted["population_pct"],
        df_sorted["random_baseline"],
        linestyle="--",
        linewidth=1,
        color="gray",
        label="Baseline"
    )

    ax.set_title("Uplift Gain Curve (Targeting Efficiency)")
    ax.set_xlabel("Targeted Population (%)", fontsize=ui["axis"]["label_size"])
    ax.set_ylabel("Cumulative Expected ASC Rate Gain", fontsize=ui["axis"]["label_size"])
    ax.tick_params(labelsize=ui["axis"]["tick_size"])
    ax.legend()

    return fig

def load_ui_config():
    with open("config/ui.yaml", "r") as f:
        return yaml.safe_load(f)

ui = load_ui_config()

st.set_page_config(
    layout=ui["page"]["layout"],
    page_title=ui["page"]["title"]
)
st.markdown(
    f"<h1 style='font-size:{ui['title']['size']}px;'> Site-of-Care Optimization Dashboard</h1>",
    unsafe_allow_html=True
)
# Load data
@st.cache_data
def load_data():
    return pd.read_csv("results/final_output.csv")

df = load_data()

# -------------------------
# Top providers
# -------------------------
st.subheader("Top Providers by Final Score")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Providers ranked by combined impact: opportunity size × likelihood of response."
    "</span>",
    unsafe_allow_html=True
)

top_n = st.slider("Top N", 5, 50, 10)

st.dataframe(
    df.sort_values("final_score", ascending=False).head(top_n)
)

# -------------------------
# Uplift distribution
# -------------------------
uplift_mean = df["uplift_score"].mean()
uplift_std = df["uplift_score"].std()
st.subheader("Uplift Score Distribution")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Distribution of estimated provider responsiveness to intervention. "
    "Higher scores indicate greater likelihood of behavior change."
    f"Mean = {uplift_mean:.4f}, Standard deviation = {uplift_std:.4f}."
    "</span>",
    unsafe_allow_html=True
)

fig, ax = plt.subplots(figsize=(ui["figure"]["width"], ui["figure"]["height"]))

ax.hist(df["uplift_score"], bins=30)

ax.set_xlabel(
    "Uplift Score",
    fontsize=ui["axis"]["label_size"]
)
ax.set_ylabel(
    "Number of Providers",
    fontsize=ui["axis"]["label_size"]
)

ax.tick_params(labelsize=ui["axis"]["tick_size"])

st.pyplot(fig)
# -------------------------
# Opportunity vs Uplift
# -------------------------
plot_df = df.copy()

x_low, x_high = plot_df["opportunity_score"].quantile([0.01, 0.99])
y_low, y_high = plot_df["uplift_score"].quantile([0.01, 0.99])

plot_df = plot_df[
    plot_df["opportunity_score"].between(x_low, x_high) &
    plot_df["uplift_score"].between(y_low, y_high)
]
st.subheader("Opportunity vs Uplift")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Providers in the top-right represent high impact and high responsiveness. "
    "Extreme outliers are excluded from this view for readability."
    "</span>",
    unsafe_allow_html=True
)

# fig, ax = plt.subplots(figsize=(ui["figure"]["width"], ui["figure"]["height"]))
# ax.scatter(plot_df["opportunity_score"], plot_df["uplift_score"])
# ax.set_xlabel("Opportunity Score", fontsize=ui["axis"]["label_size"])
# ax.set_ylabel("Uplift Score", fontsize=ui["axis"]["label_size"])




# Calculate midpoints
x_mid = plot_df["opportunity_score"].median()
y_mid = plot_df["uplift_score"].median()

fig, ax = plt.subplots(figsize=(ui["figure"]["width"], ui["figure"]["height"]))

# Scatter (lighter)
ax.scatter(
    plot_df["opportunity_score"],
    plot_df["uplift_score"],
    alpha=0.4,
    s=10
)

# # Quadrant lines
ax.axvline(x=x_mid, linestyle="--", linewidth=1, color='gray')
ax.axhline(y=y_mid, linestyle="--", linewidth=1, color='gray')

# Get axis limits
x_min, x_max = ax.get_xlim()
y_min, y_max = ax.get_ylim()

# Add padding (5–10%)
x_pad = (x_max - x_min) * 0.01
y_pad = (y_max - y_min) * 0.01

# Place labels in corners (NOT center)

# Quadrant labels (clean + readable)
ax.text(x_max - x_pad, y_max - y_pad,
        "High Impact\nHigh Response",
        fontsize=9, ha="right", va="top")

ax.text(x_max - x_pad, y_min + y_pad,
        "High Impact\nLow Response",
        fontsize=9, ha="right", va="bottom")

ax.text(x_min + x_pad, y_max - y_pad,
        "Low Impact\nHigh Response",
        fontsize=9, ha="left", va="top")

ax.text(x_min + x_pad, y_min + y_pad,
        "Low Impact\nLow Response",
        fontsize=9, ha="left", va="bottom")

ax.set_xlabel("Opportunity Score", fontsize=ui["axis"]["label_size"])
ax.set_ylabel("Uplift Score", fontsize=ui["axis"]["label_size"])
ax.tick_params(labelsize=ui["axis"]["tick_size"])
st.pyplot(fig)


# -------------------------
# POC Curve
# -------------------------
st.subheader("Uplift Gain Curve (Targeting Efficiency)")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Shows cumulative uplift captured when targeting top-ranked providers."
    "</span>",
    unsafe_allow_html=True
)

fig = plot_uplift_gain_curve(df)

st.pyplot(fig)

# -------------------------
# Segment view
# -------------------------
st.subheader("Uplift Segments")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Providers grouped by predicted responsiveness. High segment providers are most likely to respond to outreach."
    "</span>",
    unsafe_allow_html=True
)
segment_cols = [
    "procedure_volume",
    "risk_score",
    "asc_rate",
    "hopd_rate",
    "inpatient_rate",
    "cost_gap",
    "uplift_score",
]
segment_summary = df.groupby("uplift_segment")[segment_cols].mean()
st.dataframe(segment_summary)