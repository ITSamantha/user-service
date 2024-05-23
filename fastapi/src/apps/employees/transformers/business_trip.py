from src.apps.employees import models
from src.apps.employees.schemas.business_trip import BusinessTrip
from src.utils.transformer import BaseTransformer


class BusinessTripTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "employee"
        ]
        self.default_includes = []

    def transform(self, business_trip: models.BusinessTrip):
        return BusinessTrip(
            id=business_trip.id,
            start_date=business_trip.start_date,
            end_date=business_trip.end_date,
            purpose=business_trip.purpose,
            destination=business_trip.destination,
            created_at=business_trip.created_at,
            updated_at=business_trip.updated_at,
            deleted_at=business_trip.deleted_at
        )

    def include_employee(self, business_trip: models.BusinessTrip):
        from src.apps.employees.transformers.employee import EmployeeTransformer
        return self.item(business_trip.employee, EmployeeTransformer().include(["position"]))
