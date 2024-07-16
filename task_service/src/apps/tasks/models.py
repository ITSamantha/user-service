from __future__ import annotations

import datetime
from typing import Optional, List

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

    tasks: Mapped[List[Task]] = relationship("Task", back_populates="project", lazy="selectin", uselist=True)


class TaskStatus(Base):
    DONE = 1
    IN_PROCESS = 2

    __tablename__ = "task_statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True, unique=True)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True, nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    expected_completion_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    actual_completion_date: Mapped[datetime.datetime] = mapped_column(nullable=True)

    hours_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    assigned_employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL",
                   name="fk_project_id", use_alter=True), nullable=True)
    project: Mapped[Project] = relationship("Project", uselist=False,
                                            lazy="joined", back_populates="tasks")

    task_status_id: Mapped[int] = mapped_column(ForeignKey("task_statuses.id",
                                                           name="fk_task_status_id", use_alter=True),
                                                nullable=False, default=TaskStatus.IN_PROCESS)
    task_status: Mapped[TaskStatus] = relationship("TaskStatus", uselist=False, lazy="joined")

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("project_id", "title"),
    )
