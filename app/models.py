from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    currency: Mapped[str] = mapped_column(String(3))
    visit_date: Mapped[date]
    budget: Mapped[float]
    is_completed: Mapped[bool] = mapped_column(default=False)

    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="visit",
        cascade="all, delete-orphan"
    )


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    visit_id: Mapped[int] = mapped_column(ForeignKey("visits.id"))
    title: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float]

    visit: Mapped["Visit"] = relationship(back_populates="expenses")