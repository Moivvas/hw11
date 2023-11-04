from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr
from pydantic import BaseModel, Field, EmailStr

class ContactBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    additional_data: str = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    additional_data: str = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        