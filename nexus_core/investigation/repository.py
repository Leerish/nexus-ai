from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nexus_core.investigation.models import Investigation , InvestigationStatus
from nexus_core.investigation.schemas import InvestigationCreate
from datetime import datetime, timezone

def create_investigation(
    db: Session,
    data: InvestigationCreate,
) -> Investigation:
    investigation = Investigation(
        question=data.question,
        priority=data.priority,
    )

    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    return investigation


def get_investigation(
    db: Session,
    investigation_id: UUID,
) -> Investigation | None:
    statement = select(Investigation).where(
        Investigation.id == investigation_id
    )

    return db.scalar(statement)

def update_investigation_result(
    db: Session,
    investigation: Investigation,
    result: dict,
    confidence_score: float | None = None,
) -> Investigation:
    investigation.result = result
    investigation.confidence_score = confidence_score
    investigation.status = InvestigationStatus.COMPLETED
    investigation.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(investigation)

    return investigation

def list_investigations(
    db: Session,
    limit: int = 20,
) -> list[Investigation]:

    statement = (
        select(Investigation)
        .order_by(Investigation.created_at.desc())
        .limit(limit)
    )

    return list(db.scalars(statement).all())