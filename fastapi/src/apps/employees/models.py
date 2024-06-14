import datetime
from typing import List, Optional

from sqlalchemy import Integer, ForeignKey, String, CheckConstraint, ForeignKeyConstraint
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


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    login: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id", ondelete="SET NULL", name="fk_employee_unit_id"),
                                         nullable=True)
    unit: Mapped["Unit"] = relationship(uselist=False, foreign_keys=[unit_id],
                                        back_populates="employees", lazy="joined")
    position_id: Mapped[int] = mapped_column(ForeignKey("employee_positions.id", ondelete="SET NULL"), nullable=True)
    position: Mapped["EmployeePosition"] = relationship(uselist=False, lazy="subquery")

    vacations: Mapped[List["Vacation"]] = relationship(uselist=True, lazy="subquery")  # TODO: CHECK
    business_trips: Mapped[List["BusinessTrip"]] = relationship(uselist=True, lazy="subquery")  # TODO: CHECK

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    director_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id", name="fk_unit_director_id"),
                                                       nullable=True)
    director: Mapped[Optional["Employee"]] = relationship(uselist=False, foreign_keys=[director_id], lazy="joined")

    employees: Mapped[List["Employee"]] = relationship(uselist=True, foreign_keys=[Employee.unit_id], lazy="joined")


class VacationReason(Base):
    __tablename__ = "vacation_reasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)


class Vacation(Base):
    __tablename__ = "vacations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    vacation_type_id: Mapped[int] = mapped_column(ForeignKey("vacation_types.id", ondelete="SET NULL"), nullable=True)
    vacation_type: Mapped[VacationType] = relationship(uselist=False, lazy="joined")

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship(uselist=False, lazy="joined")

    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)

    vacation_reason_id: Mapped[int] = mapped_column(ForeignKey("vacation_reasons.id", ondelete="SET NULL"),
                                                    nullable=True)
    vacation_reason: Mapped[VacationReason] = relationship(uselist=False, lazy="joined")

    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

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
    employee: Mapped["Employee"] = relationship(uselist=False, lazy="joined")

    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)

    purpose: Mapped[str] = mapped_column(String, nullable=False)

    destination: Mapped[str] = mapped_column(String, nullable=False)

    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint(start_date <= end_date, name='check_dates'),
    )
