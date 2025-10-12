from pydantic import BaseModel, Field
from datetime import datetime


class BaseCustomerInfo(BaseModel):
    national_code: str| None = None
    email: str|None = None



class CustomerInfo(BaseModel):
    f_name: str | None = None
    l_name: str | None = None
    national_code: str | None = None
    city: str | None = None
    plan_type: str | None = None
    phone_number: str | None = None
    email: str | None = None


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
    created_at: datetime | None = None


class EmailInfo(BaseModel):
    national_code: str | None = Field(default=None, description="National code")
    email_type: str | None = Field(default="rejection", description="Email type")
    email: str = Field(..., description="Email address") 
    phone_number: str | None = Field(default='None', description="Phone number")

class NA(BaseModel):
    national_code: str | None = None

class Email(BaseModel):
    email: str | None = None


class OTPModel(BaseModel):
    OTP_code: str | None = None



class SimCardInfo(BaseModel):
    plan_type: str | None = None
