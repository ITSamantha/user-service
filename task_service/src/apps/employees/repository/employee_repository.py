from sqlalchemy import select, or_, and_

from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository, ModelType


class EmployeeRepository(SqlAlchemyRepository):

    async def search(self, first_name: str = None, last_name: str = None, patronymic: str = None, login: str = None,
                     email: str = None, unique: bool = False) -> ModelType:
        async with self._session_factory() as session:

            criteria = []

            if first_name:
                criteria.append(self.model.first_name.ilike(first_name))

            if last_name:
                criteria.append(self.model.last_name.ilike(last_name))

            if patronymic:
                criteria.append(self.model.patronymic.ilike(patronymic))

            if login:
                criteria.append(self.model.login.ilike(login))

            if email:
                criteria.append(self.model.email.ilike(email))

            stmt = select(self.model).filter(and_(*criteria))

            row = await session.execute(stmt)

            if unique:
                row = row.unique()

            return row.scalars().all()
