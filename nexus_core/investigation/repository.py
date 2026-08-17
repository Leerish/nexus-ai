from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nexus_core.investigation.models import Investigation
from nexus_core.investigation.schemas import InvestigationCreate


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