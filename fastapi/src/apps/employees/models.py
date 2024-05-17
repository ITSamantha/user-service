import datetime
from typing import List, Optional

from sqlalchemy import Integer, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base


# todo: indexes
# todo: lazy

class EmployeePosition(Base):
    __tablename__ = "employee_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)


class VacationType(Base):
    __tablename__ = "vacation_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    director_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    director: Mapped[Optional["Employee"]] = relationship(uselist=False)

    employees: Mapped[List["Employee"]] = relationship(uselist=True)


class Employee(Base):
    __tablename__ = "employees"

    # todo: read about table args
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    login: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    unit: Mapped["Unit"] = relationship(uselist=False)

    position_id: Mapped[int] = mapped_column(ForeignKey("employee_positions.id"), nullable=False)
    position: Mapped["EmployeePosition"] = relationship(uselist=False)

    vacations: Mapped[List["Vacation"]] = relationship(uselist=True)
    business_trips: Mapped[List["BusinessTrip"]] = relationship(uselist=True)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)


class Vacation(Base):
    __tablename__ = "vacations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    vacation_type_id: Mapped[int] = mapped_column(ForeignKey("vacation_types.id"), nullable=False)
    vacation_type: Mapped["VacationType"] = relationship(uselist=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship(uselist=False)

    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)

    reason: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint(start_date <= end_date, name='check_dates'),
    )


class BusinessTrip(Base):
    __tablename__ = "business_trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship(uselist=False)

    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)

    purpose: Mapped[str] = mapped_column(String, nullable=False)

    destination: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint(start_date <= end_date, name='check_dates'),
    )
