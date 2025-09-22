from pydantic import BaseModel

class CustomerInfo(BaseModel):
    f_name: str | None = None
    l_name: str | None = None
    national_code: str | None = None
    city: str | None = None
    plan_type: str | None = None


class PhoneNumber(BaseModel):
    national_code: str | None = None
    phone_number: str | None = None


class BillingRequest(BaseModel):
    national_code: str | None = None
    plan_type: str | None = None
    phone_number: str | None = None

class BillingInfo(BaseModel):
    national_code: str | None = None
    plan_type: str | None = None
    phone_number: str | None = None
    total: int | None = None
    bill_id: str | None = None