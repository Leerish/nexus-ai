from sqlalchemy.orm import Session

from nexus_core.investigation.models import Investigation
from nexus_core.investigation.repository import (
    update_investigation_result,
)
from nexus_core.investigation.serialization import (
    serialize_investigation_state,
)
from nexus_core.reasoning.graph import investigation_graph


def run_investigation(
    db: Session,
    investigation: Investigation,
) -> Investigation:
    state = investigation_graph.invoke(
        {
            "investigation_id": str(investigation.id),
            "question": investigation.question,
            "tasks": [],
            "results": [],
            "conclusion": None,
            "root_cause_analysis": None,
            "report": None,
        }
    )

    serialized = serialize_investigation_state(state)

    confidence_score = None

    if state.get("conclusion") is not None:
        claim_assessment = state["conclusion"].claim_assessment

        if claim_assessment is not None:
            confidence_score = claim_assessment.confidence

    return update_investigation_result(
        db=db,
        investigation=investigation,
        result=serialized,
        confidence_score=confidence_score,
    )