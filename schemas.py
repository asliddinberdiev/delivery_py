from pydantic import BaseModel
from typing import Optional

from config.env import cfg

class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "example@gmail.com",
                "password": "pass123",
                "is_staff": False,
                "is_active": False
            }
        }

class SigninModel(BaseModel):
    username_or_email: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "username",
                "password": "pass123"
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = cfg.auth_secret_key