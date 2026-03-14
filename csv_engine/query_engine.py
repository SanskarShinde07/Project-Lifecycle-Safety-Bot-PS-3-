import pandas as pd

monthly_df = pd.read_csv(
    "data/csv_docs/construction_monthly_metrics_numeric.csv"
)

baseline_df = pd.read_csv(
    "data/csv_docs/construction_topic_baselines_numeric.csv"
)


def normalize(text):
    return text.lower().replace("&", "and").strip()


def get_baseline_metric(topic, metric):

    result = baseline_df[baseline_df["topic_name"] == topic]

    if result.empty:
        print("Topic not found:", topic)
        return None

    if metric not in baseline_df.columns:
        print("Metric not found:", metric)
        return None

    return result.iloc[0][metric]


def get_monthly_metric(topic, month, metric):

    result = monthly_df[
        (monthly_df["topic_name"].str.contains(topic, case=False))
        & (monthly_df["period_month"] == month)
    ]

    if result.empty:
        return "No data found."

    return result.iloc[0][metric]

def get_all_topics():
    return baseline_df["topic_name"].tolist()