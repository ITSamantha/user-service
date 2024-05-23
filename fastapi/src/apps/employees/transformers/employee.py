from src.apps.employees.schemas.employee import EmployeePosition, Unit, Employee
from src.apps.employees.transformers.business_trip import BusinessTripTransformer
from src.apps.employees.transformers.vacation import VacationTransformer
from src.utils.transformer import BaseTransformer
from src.apps.employees import models


class EmployeePositionTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, employee_position: models.EmployeePosition):
        return EmployeePosition(
            id=employee_position.id,
            title=employee_position.title
        )


class EmployeeTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "unit",
            "vacations",
            "business_trips"
        ]
        self.default_includes = [
            "position"
        ]

    def transform(self, employee: models.Employee):
        return Employee(
            id=employee.id,
            last_name=employee.last_name,
            first_name=employee.first_name,
            patronymic=employee.patronymic,
            login=employee.login,
            email=employee.email,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            deleted_at=employee.deleted_at
        )

    def include_unit(self, employee: models.Employee):
        return self.item(employee.unit, UnitTransformer())

    def include_position(self, employee: models.Employee):
        return self.item(employee.position, EmployeePositionTransformer())

    def include_vacations(self, employee):
        return self.collection(employee.vacations, VacationTransformer())

    def include_business_trips(self, employee):
        return self.collection(employee.business_trips, BusinessTripTransformer())


class UnitTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "director",
            "employees"
        ]
        self.default_includes = []

    def transform(self, unit: models.Unit):
        return Unit(
            id=unit.id,
            title=unit.title
        )

    def include_employees(self, unit: models.Unit):
        return self.collection(unit.employees, EmployeeTransformer().include(["position"]))

    def include_director(self, unit: models.Unit):
        return self.item(unit.director, EmployeeTransformer().include(["position"]))
