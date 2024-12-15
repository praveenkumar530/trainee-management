# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
#
# class UserDataRequest(BaseModel):
#     first_name: str = Field(..., title="First Name", max_length=50)
#     last_name: str = Field(..., title="Last Name", max_length=50)
#     email: EmailStr = Field(..., title="Email Address")
#     phone: Optional[str] = Field(None, title="Phone Number", pattern=r"^\+?\d{10,15}$")  # Optional with phone validation
#     role_id: int = Field(1, title="Role ID")
#
#     class Config:
#         orm_mode = True  # Allows the model to work seamlessly with ORM objects like SQLAlchemy


from pydantic import BaseModel, EmailStr

class UserDataRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role_id: int
