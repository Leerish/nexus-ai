from nexus_core.reasoning.state import (
    InvestigationState,
    TaskResult,
)


def aggregate_results(
    state: InvestigationState,
) -> dict:
    return {
        "results": state["results"],
    }