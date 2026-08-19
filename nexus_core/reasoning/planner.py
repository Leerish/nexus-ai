import json

from langchain_ollama import ChatOllama

from nexus_core.reasoning.state import (
    InvestigationTask,
    PlannerOutput,
)


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)


PLANNER_PROMPT = """
You are the investigation planning component of Nexus AI.

Break the investigation question into concrete analytical tasks.

IMPORTANT RULES:

1. Create only tasks that can be executed by the analysis executor.
2. Do NOT create a root_cause task.
3. Root-cause reasoning happens automatically after evidence synthesis.
4. Do NOT create generic evidence_gathering tasks unless there is an
   implemented evidence source available.
5. Prefer concrete data-analysis and temporal-analysis tasks.
6. Every task must directly contribute evidence toward answering the question.
7. Avoid duplicate or redundant tasks.
8. Return between 1 and 6 tasks.

Allowed task types:
- data_analysis
- temporal_analysis

Available analyses:

- churn_by_segment
  Use for analyzing churn differences across customer segments.

- churn_satisfaction
  Use for analyzing the relationship between satisfaction scores
  and churn.

- product_change_churn
  Use for analyzing churn by number of product changes.

- temporal_churn
  Use for analyzing churn trends across quarters or time periods.

IMPORTANT:
Only create tasks that map directly to one of the available analyses above.

Do NOT create tasks involving:
- customer feedback
- support tickets
- marketing campaigns
- pricing
- product events
- other external evidence sources

unless an analysis for that source is explicitly available.

For churn investigations, when the following analyses are available,
prefer including all relevant analyses:

- churn by customer segment
- churn by satisfaction
- churn by product changes
- temporal churn trends

Do not omit a relevant analysis merely because another analysis appears
sufficient. The goal is comprehensive evidence collection before synthesis.

Return ONLY valid JSON:

{{
    "tasks": [
        {{
            "type": "data_analysis",
            "description": "Analyze churn by customer segment"
        }}
    ]
}}

Investigation question:
{question}
"""


def plan_investigation(
    question: str,
) -> list[InvestigationTask]:
    prompt = PLANNER_PROMPT.format(
        question=question
    )

    response = llm.invoke(prompt)

    raw_output = response.content.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Planner returned invalid JSON: {raw_output}"
        ) from exc

    planner_output = PlannerOutput.model_validate(
        parsed
    )

    return planner_output.tasks