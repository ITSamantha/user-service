from typing import Type, TypeVar, Optional, Generic, List

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.base import Base
from src.utils.repository.base_repository import AbstractRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD repository for models."""

    def __init__(self, session: AsyncSession, model: Type[ModelType] = None):
        self.model = model
        self._session_factory = session

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session_factory() as session:
            obj_create_data = data.model_dump(exclude_none=True, exclude_unset=True)
            instance = self.model(**obj_create_data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def bulk_create(self, data: List[CreateSchemaType]) -> ModelType:
        async with self._session_factory() as session:
            objects = [self.model(**d.model_dump(exclude_none=True, exclude_unset=True)) for d in data]
            session.add_all(objects)
            await session.commit()
            return objects

    async def update(self, data: UpdateSchemaType, exclude_none=True, exclude_unset=True, **filters) -> ModelType:
        async with self._session_factory() as session:
            stmt = update(self.model).values(
                **data.model_dump(exclude_none=exclude_none, exclude_unset=exclude_unset)).filter_by(
                **filters).returning(
                self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session_factory() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()

    async def get_single(self, **filters) -> Optional[ModelType]:
        async with self._session_factory() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            return row.scalar_one_or_none()

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            **filters
    ) -> list[ModelType]:
        async with self._session_factory() as session:
            order_column = getattr(self.model, order, None)

            if order_column is None:
                raise ValueError(f"Invalid order column: {order}")

            stmt = select(self.model).filter_by(**filters).order_by(order_column).limit(limit).offset(offset)
            row = await session.execute(stmt)
            return row.scalars().all()
