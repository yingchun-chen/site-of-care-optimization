from sklearn.cluster import KMeans

def segment_providers(df):
    features = ["procedure_volume", "asc_rate", "avg_cost", "risk_score"]

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["segment"] = kmeans.fit_predict(df[features])

    return df