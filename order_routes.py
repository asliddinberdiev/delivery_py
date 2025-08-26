from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from models import User, Product, Order
from schemas import OrderModel, OrderStatusModel
from database import session, engine

order_router = APIRouter(prefix="/orders", tags=["ORDER"])

@order_router.get("")
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        pass
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return {"message": "success"}