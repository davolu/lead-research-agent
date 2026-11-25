"""Run the Langflow "Lead Research Agent" flow for one company and print the brief.

Set these environment variables first (never hard-code them):
  LANGFLOW_URL      e.g. http://localhost:7860
  FLOW_ID           the flow's ID (Share > API access in Langflow)
  LANGFLOW_API_KEY  a Langflow API key (Settings > Langflow API Keys)

Usage:  python predict.py "Figma"
"""
import os
import sys
import uuid

import requests


def run(company: str) -> str:
    url = f"{os.environ['LANGFLOW_URL']}/api/v1/run/{os.environ['FLOW_ID']}?stream=false"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ["LANGFLOW_API_KEY"]}
    payload = {
        "input_value": company,
        "input_type": "chat",
        "output_type": "chat",
        "session_id": str(uuid.uuid4()),  # fresh session: no memory carried between companies
    }
    response = requests.post(url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    data = response.json()
    return data["outputs"][0]["outputs"][0]["outputs"]["message"]["message"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Usage: python predict.py "Company name"')
    print(run(sys.argv[1]))
