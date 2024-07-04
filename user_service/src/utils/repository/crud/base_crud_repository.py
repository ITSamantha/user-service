from typing import Type, TypeVar, Optional, Generic, List

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import class_mapper, RelationshipProperty, selectinload, joinedload, subqueryload

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
            obj_create_data = data.model_dump(exclude_none=False, exclude_unset=True)
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

    async def update(self, data: UpdateSchemaType, exclude_none=False, exclude_unset=False, **filters) -> ModelType:
        async with self._session_factory() as session:
            instance_data = data.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_none)
            stmt = update(self.model).values(
                **instance_data).filter_by(
                **filters).returning(
                self.model)
            res = await session.execute(stmt)
            res = res.unique()
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> bool:
        async with self._session_factory() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()
            return True

    async def get_single(self, **filters) -> Optional[Type[Base]]:
        async with self._session_factory() as session:  # type: AsyncSession
            stmt = select(self.model).filter_by(**filters)
            stmt = self._apply_eager_loading(stmt)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    def _apply_eager_loading(self, stmt):
        # Get all relationships for the model
        mapper = class_mapper(self.model)
        for prop in mapper.iterate_properties:
            if isinstance(prop, RelationshipProperty):
                stmt = stmt.options(subqueryload(getattr(self.model, prop.key)))
        return stmt

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            unique: bool = False,
            **filters
    ) -> list[ModelType]:
        async with self._session_factory() as session:
            order_column = getattr(self.model, order, None)

            if order_column is None:
                raise ValueError(f"Invalid order column: {order}")

            stmt = select(self.model).filter_by(**filters).order_by(order_column).limit(limit).offset(offset)

            row = await session.execute(stmt)

            if unique:
                row = row.unique()

            return row.scalars().all()
