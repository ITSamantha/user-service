from sqlalchemy import select, or_, and_

from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository, ModelType


class TaskRepository(SqlAlchemyRepository):

    async def search(self, title: str = None, description: str = None, unique: bool = False) -> ModelType:
        async with self._session_factory() as session:

            criteria = []

            if title:
                criteria.append(self.model.title.ilike(title))

            if description:
                criteria.append(self.model.description.ilike(description))

            stmt = select(self.model).filter(and_(*criteria))

            row = await session.execute(stmt)

            if unique:
                row = row.unique()

            return row.scalars().all()
