from rag.retriever import get_retriever
from router.source_router import route_question
from csv_engine.query_engine import get_baseline_metric, get_monthly_metric
from router.topic_detector import detect_topic
from openai import AzureOpenAI
from csv_engine.csv_agent import ask_csv

import os

metric_map = {
    "risk": "inherent_risk_score",
    "likelihood": "likelihood_score",
    "severity": "severity_potential_score",
    "training": "baseline_training_hours",
    "permit": "permit_required_pct",
    "inspection": "inspections_completed",
    "trir": "trir_value",
    "dart": "dart_value",
    "compliance": "compliance_score_pct"
}
retriever = get_retriever()

def detect_metric(question):

    q = question.lower()

    for keyword, metric in metric_map.items():
        if keyword in q:
            return metric

    return None
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)


def ask_llm(context, question):

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are a construction safety assistant. Only answer using the exact information in the context. Do not modify titles or roles."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    )

    return response.choices[0].message.content


def ask_question(question):
    topic = detect_topic(question)
    route = route_question(question)
    metric = detect_metric(question)
    print("Detected Topic:", topic)
    print("Detected Metric:", metric)
    if route == "TXT":

        docs = retriever.invoke(question)
        context = docs[0].page_content

        answer = ask_llm(context, question)

        return f"{answer}\n\n---\nSource: TXT Document"

    if route == "CSV":
        return ask_csv(question)

    if route == "HYBRID":

        docs = retriever.invoke(question)

        context = docs[0].page_content

        risk = get_baseline_metric(topic, "inherent_risk_score")

        combined_context = f"""
        Document Information:
        {context}

        Numeric Data:
        Inherent risk score: {risk}
        """

        return f"""
    {ask_llm(combined_context, question)}

---
Sources:
• TXT Knowledge Base
• Baseline Metrics CSV (construction_topic_baselines_numeric.csv)
"""