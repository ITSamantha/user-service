import datetime
from typing import List, Union

from src.apps.employees import models
from src.apps.employees.schemas.business_trip import CreateBusinessTrip
from src.apps.employees.schemas.vacation import CreateVacation
from src.core.database.session_manager import db_manager
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository


# TODO: REMOVE DUPLICATES
async def check_business_trips_valid_dates(data: Union[CreateBusinessTrip, CreateVacation]):
    employee_business_trips: List[models.BusinessTrip] = await SqlAlchemyRepository(db_manager.get_session,
                                                                                    model=models.BusinessTrip).get_multi(
        employee_id=data.employee_id, unique=True)

    for business_trip in employee_business_trips:

        business_trip_start_date: datetime.date = business_trip.start_date
        business_trip_end_date: datetime.date = business_trip.end_date

        if not (data.end_date < business_trip_start_date or data.start_date > business_trip_end_date):
            raise Exception(
                f"Date of business trip with id={business_trip.id} "
                f"date from {business_trip_start_date} to {business_trip_end_date} "
                f"crosses with the given data from {data.start_date} to {data.end_date}.")


async def check_vacations_valid_dates(data: Union[CreateBusinessTrip, CreateVacation]):
    employee_vacations: List[models.Vacation] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.Vacation).get_multi(
        employee_id=data.employee_id, unique=True)

    for vacation in employee_vacations:

        vacation_start_date: datetime.date = vacation.start_date
        vacation_end_date: datetime.date = vacation.end_date

        if not (data.end_date < vacation_start_date or data.start_date > vacation_end_date):
            raise Exception(
                f"Date of vacation with id={vacation.id} "
                f"date from {vacation_start_date} to {vacation_end_date} "
                f"crosses with the given data from {data.start_date} to {data.end_date}.")
