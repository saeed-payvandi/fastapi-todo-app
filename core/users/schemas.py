from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime


class UserBaseSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., max_length=50, description="password of the user")


class UserLoginSchema(UserBaseSchema):
    pass


class UserRegisterSchema(UserBaseSchema):
    password_confirm: str = Field(..., description="confirm password of the user")

    @field_validator("password_confirm")
    @classmethod
    def check_password_match(cls, password_confirm, info: ValidationInfo):
        if password_confirm != info.data.get("password"):
            raise ValueError("password does not match")
        return password_confirm
