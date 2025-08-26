import uuid

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
                "username_or_email": "username",
                "password": "pass123"
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = cfg.auth_secret_key

class OrderModel(BaseModel):
    id: Optional[str]
    user_id: str
    product_id: str
    status: Optional[str] = "PENDING"
    quantity: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "b730fe54-7083-46fd-848e-9eb2ff4a4645",
                "product_id": "01842e26-0700-4576-b97b-862d74768827",
                "quantity": 1
            }
        }

class OrderStatusModel(BaseModel):
    id: str
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01842e26-0700-4576-b97b-862d74768827",
                "status": "PENDING"
            }
        }