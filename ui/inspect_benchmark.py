# filename: inspect_benchmark.py
# execution: true
from openai_server.agent_tools.ask_question_about_documents import ask_question_about_documents

response = ask_question_about_documents(
    query="Please describe the structure of this JSON file. What are the main keys and what kind of data does it contain? Provide examples of a few entries to help understand the format.",
    files=["benchmark.json"]
)