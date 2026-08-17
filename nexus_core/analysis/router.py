
from nexus_core.reasoning.state import InvestigationTask


def resolve_analysis(task):
    description = task.description.lower()

    if (
        "temporal" in description
        or "trend" in description
        or "quarter" in description
        or "time period" in description
        or "past three quarters" in description
    ):
        return "temporal_churn"

    if "segment" in description:
        return "churn_by_segment"

    if "satisfaction" in description:
        return "churn_satisfaction"

    if "product" in description:
        return "product_change_churn"

    raise ValueError(
        f"Unsupported analysis task: {task.description}"
    )