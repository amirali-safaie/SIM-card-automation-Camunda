from pydantic import BaseModel

class CustomerInfo(BaseModel):
    f_name: str | None = None
    l_name: str | None = None
    national_code: str | None = None
    city: str | None = None
    plan_type: str | None = None


