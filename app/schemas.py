from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class VisitCreate(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    currency: str = Field(min_length=3, max_length=3)
    visit_date: date
    budget: float = Field(gt=0)


class VisitUpdate(BaseModel):
    country: str | None = Field(default=None, min_length=1, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    visit_date: date | None = None
    budget: float | None = Field(default=None, gt=0)
    is_completed: bool | None = None


class VisitOut(VisitCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_completed: bool


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)


class ExpenseOut(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visit_id: int