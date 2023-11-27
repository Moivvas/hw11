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
    user_id: int = Field(1, ge=0)

    class Config:
        orm_mode = True

class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    additional_data: str = None
    created_at: datetime
    updated_at: datetime
    user_id: int = Field(1, ge=0)

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RequestEmail(BaseModel):
    email: EmailStr