# Site-of-Care Optimization | Healthcare Analytics Project

## Overview

A healthcare analytics project that identifies provider-level opportunities to shift procedures from higher-cost hospital settings to lower-cost ambulatory surgical centers (ASC).

This project simulates a value-based care use case by integrating provider benchmarking, opportunity scoring, predictive modeling, uplift modeling, and interactive dashboarding to support data-driven decision-making.

> Designed to simulate real-world value-based care use cases using synthetic and conceptual data models.


## Tech Stack
- **Languages:** Python, SQL  
- **Data & ML:** pandas, scikit-learn  
- **Visualization:** Matplotlib, Seaborn, Streamlit
- **Config & Dev:** YAML, GitHub  

## Key Features

- Provider benchmarking against regional peers
- Opportunity scoring based on utilization and cost gaps
- Predictive modeling for high-cost site-of-care patterns
- Uplift modeling to estimate provider responsiveness to intervention
- Streamlit dashboard for interactive exploration

## Design and Methodoligy
- Simulation framework using synthetic data and conceptual healthcare data models
- Feature engineering for provider-level cost and utilization patterns
- Supervised learning models for risk prediction
- Uplift modeling to estimate incremental impact of interventions
- Visualization of opportunity vs. impact trade-offs
  
## Results Preview
![alt text](results/opportunity_vs_uplift.png)


## Project Structure

```text
siteofshift/
├── src/siteofshift/
├── config/
│   └── ui.yaml
├── data/
├── results/
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

## How to Run
### Using uv  
  
```bash  
# Sync dependencies  
uv sync  
  
# Run tests  
PYTHONPATH=src uv run --active pytest  
  
# Run pipeline  
PYTHONPATH=src uv run --active python -m siteofshift.main  
  
# Run dashboard  
PYTHONPATH=src uv run --active streamlit run src/siteofshift/dashboard.py
```


### Using Docker

```bash
# Build image
docker build -t siteofshift .

# Run pipeline in Docker
docker run --rm -v $(pwd)/results:/app/results siteofshift

# Run dashboard in Docker
docker run --rm -p 8501:8501 \
  -v $(pwd)/results:/app/results \
  siteofshift \
  uv run python -m streamlit run src/siteofshift/dashboard.py \
  --server.address 0.0.0.0 \
  --server.port 8501
```


## Author 
Yingchun Chen
Senior Healthcare Data Analyst | Data Science & Analytics

## LICENCE
MIT License