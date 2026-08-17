import json

from langchain_ollama import ChatOllama

from nexus_core.reasoning.state import PlannerOutput


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)


PLANNER_PROMPT = """
You are the planning component of Nexus AI.

Your job is NOT to answer the user's question.

Your job is to decompose the question into concrete investigation tasks.

Allowed task types:

- data_analysis
- temporal_analysis
- root_cause
- evidence_gathering

Return ONLY a valid JSON object in this format:

{{
  "tasks": [
    {{
      "type": "data_analysis",
      "description": "Analyze churn by customer segment"
    }}
  ]
}}

Generate between 1 and 8 tasks.

User question:
{question}
"""


def plan_investigation(question: str) -> list[dict]:
    prompt = PLANNER_PROMPT.format(question=question)

    response = llm.invoke(prompt)

    raw_output = response.content.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Planner returned invalid JSON: {raw_output}"
        ) from exc

    planner_output = PlannerOutput.model_validate(parsed)

    return planner_output.tasks