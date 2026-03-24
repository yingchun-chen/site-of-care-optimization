import yaml
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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
st.subheader("Uplift Score Distribution")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Distribution of estimated provider responsiveness to intervention. "
    "Higher scores indicate greater likelihood of behavior change."
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
st.subheader("Opportunity vs Uplift")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Providers in the top-right represent high impact and high responsiveness."
    "</span>",
    unsafe_allow_html=True
)

fig, ax = plt.subplots(figsize=(ui["figure"]["width"], ui["figure"]["height"]))

ax.scatter(df["opportunity_score"], df["uplift_score"])

ax.set_xlabel("Opportunity Score", fontsize=ui["axis"]["label_size"])
ax.set_ylabel("Uplift Score", fontsize=ui["axis"]["label_size"])
ax.tick_params(labelsize=ui["axis"]["tick_size"])

st.pyplot(fig)

# -------------------------
# POC Curve
# -------------------------
st.subheader("POC Curve (Targeting Efficiency)")
st.markdown(
    f"<span style='font-size:{ui['description']['size']}px'>"
    "Shows cumulative uplift captured when targeting top-ranked providers."
    "</span>",
    unsafe_allow_html=True
)

fig, ax = plt.subplots(figsize=(ui["figure"]["width"], ui["figure"]["height"]))

df_sorted = df.sort_values("uplift_score", ascending=False).reset_index(drop=True)
df_sorted["cum_gain"] = df_sorted["uplift_score"].cumsum()
df_sorted["population_pct"] = (df_sorted.index + 1) / len(df_sorted)

ax.plot(df_sorted["population_pct"], df_sorted["cum_gain"])

ax.set_xlabel("Targeted Population (%)", fontsize=ui["axis"]["label_size"])
ax.set_ylabel("Cumulative Uplift Gain", fontsize=ui["axis"]["label_size"])
ax.tick_params(labelsize=ui["axis"]["tick_size"])

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
st.dataframe(
    df.groupby("uplift_segment").mean(numeric_only=True)
)
