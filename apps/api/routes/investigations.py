from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.dependencies import get_db
from nexus_core.investigation.repository import (
    create_investigation,
    get_investigation,
)
from nexus_core.investigation.schemas import (
    InvestigationCreate,
    InvestigationResponse,
)


router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"],
)


@router.post(
    "",
    response_model=InvestigationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: InvestigationCreate,
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    return create_investigation(db, data)


@router.get(
    "/{investigation_id}",
    response_model=InvestigationResponse,
)
def get(
    investigation_id: UUID,
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    investigation = get_investigation(db, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investigation not found",
        )

    return investigation