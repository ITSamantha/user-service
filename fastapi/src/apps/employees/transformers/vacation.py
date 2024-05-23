from src.apps.employees import models
from src.apps.employees.schemas.vacation import VacationReason, VacationType, Vacation

from src.utils.transformer import BaseTransformer


class VacationTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "employee",
            "vacation_reason",
            "vacation_type"
        ]
        self.default_includes = []

    def transform(self, vacation: models.Vacation):
        return Vacation(
            id=vacation.id,
            start_date=vacation.start_date,
            comment=vacation.comment,
            end_date=vacation.end_date,
            created_at=vacation.created_at,
            updated_at=vacation.updated_at,
            deleted_at=vacation.deleted_at
        )

    def include_vacation_type(self, vacation: models.Vacation):
        return self.item(vacation.vacation_type, VacationTypeTransformer())

    def include_vacation_reason(self, vacation: models.Vacation):
        return self.item(vacation.vacation_reason, VacationReasonTransformer())

    def include_employee(self, vacation: models.Vacation):
        from src.apps.employees.transformers.employee import EmployeeTransformer
        return self.item(vacation.employee, EmployeeTransformer().include(["position"]))


class VacationTypeTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, vacation_type: models.VacationType):
        return VacationType(
            id=vacation_type.id,
            title=vacation_type.title
        )


class VacationReasonTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, vacation_reason: models.VacationReason):
        return VacationReason(
            id=vacation_reason.id,
            title=vacation_reason.title
        )
