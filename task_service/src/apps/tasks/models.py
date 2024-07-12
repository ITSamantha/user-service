from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True, unique=True)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    tasks: Mapped[Task] = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True, nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    assigned_employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL",
                   name="fk_project_id", use_alter=True), nullable=True)
    project: Mapped[Project] = relationship("Project", uselist=False,
                                            lazy="joined", back_populates="tasks")

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("project_id", "title"),
    )
