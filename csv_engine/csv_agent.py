import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import AzureChatOpenAI

# Load CSVs
baseline_df = pd.read_csv("data/csv_docs/construction_topic_baselines_numeric.csv")
monthly_df = pd.read_csv("data/csv_docs/construction_monthly_metrics_numeric.csv")

# Azure OpenAI LLM
llm = AzureChatOpenAI(
    azure_endpoint="https://vcon.openai.azure.com/",
    api_key="EfwhbUa3MrbLrioEAyALwcjwffIAOQzr6rtdeRXbTvgROOyrl9pmJQQJ99CAACYeBjFXJ3w3AAABACOGUCez",
    azure_deployment="gpt-4o",
    api_version="2024-12-01-preview",
    temperature=0
)

# Create dataframe agent
agent = create_pandas_dataframe_agent(
    llm,
    [baseline_df, monthly_df],
    verbose=True,
    allow_dangerous_code=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# Function used by chatbot
def ask_csv(question):
    return agent.run(question)