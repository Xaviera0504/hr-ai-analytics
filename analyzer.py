import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def generate_hr_insights(data_summary: str):
    """
    Send HR data summary to Claude and get plain-English insights.
    Returns insights text and the prompt used (for audit trail).
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""You are an expert HR analyst. Below is a summary of workforce data from an organization.

Write a clear, plain-English report for a non-technical HR manager or business leader.
Structure your response exactly like this:

## Workforce Overview
2-3 sentences summarizing the overall workforce health.

## Top 3 Risks
For each risk: what it is, why it matters, and which department or group is most affected.

## Top 3 Opportunities
For each opportunity: what it is and what action could improve outcomes.

## Recommended Next Steps
3 concrete actions the HR team should take in the next 30 days.

Keep the language simple. No jargon. Every insight should connect to a business outcome.

Here is the workforce data summary:
{data_summary}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text, prompt
