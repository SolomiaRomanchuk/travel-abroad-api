from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Visit, Expense
from app.schemas import (
    VisitCreate, VisitUpdate, VisitOut,
    ExpenseCreate, ExpenseOut
)

router = APIRouter(prefix="/visits", tags=["visits"])


def get_visit_or_404(visit_id: int, db: Session) -> Visit:
    visit = db.get(Visit, visit_id)
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.get("", response_model=list[VisitOut])
def list_visits(
    country: str | None = None,
    is_completed: bool | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Visit)

    if country is not None:
        query = query.where(Visit.country == country)

    if is_completed is not None:
        query = query.where(Visit.is_completed == is_completed)

    query = query.order_by(Visit.id).limit(limit).offset(offset)
    return db.scalars(query).all()


@router.get("/{visit_id}", response_model=VisitOut)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    return get_visit_or_404(visit_id, db)


@router.post("", response_model=VisitOut, status_code=201)
def create_visit(data: VisitCreate, db: Session = Depends(get_db)):
    visit = Visit(**data.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@router.patch("/{visit_id}", response_model=VisitOut)
def update_visit(
    visit_id: int,
    data: VisitUpdate,
    db: Session = Depends(get_db),
):
    visit = get_visit_or_404(visit_id, db)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(visit, field, value)

    db.commit()
    db.refresh(visit)
    return visit


@router.delete("/{visit_id}", status_code=204)
def delete_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = get_visit_or_404(visit_id, db)
    db.delete(visit)
    db.commit()
    return Response(status_code=204)


@router.post("/{visit_id}/expenses", response_model=ExpenseOut, status_code=201)
def add_expense(
    visit_id: int,
    data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    get_visit_or_404(visit_id, db)

    expense = Expense(visit_id=visit_id, **data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("/{visit_id}/expenses", response_model=list[ExpenseOut])
def list_expenses(visit_id: int, db: Session = Depends(get_db)):
    visit = get_visit_or_404(visit_id, db)
    return visit.expenses