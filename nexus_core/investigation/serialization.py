from typing import Any

from nexus_core.reasoning.state import InvestigationState


def serialize_investigation_state(
    state: InvestigationState,
) -> dict[str, Any]:
    return {
        "tasks": [
            task.model_dump(mode="json")
            for task in state["tasks"]
        ],
        "results": [
            result.model_dump(mode="json")
            for result in state["results"]
        ],
        "conclusion": (
            state["conclusion"].model_dump(mode="json")
            if state["conclusion"] is not None
            else None
        ),
        "root_cause_analysis": (
            state["root_cause_analysis"].model_dump(mode="json")
            if state["root_cause_analysis"] is not None
            else None
        ),
        "report": state.get("report"),
    }