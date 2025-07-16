from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from schemas import Settings
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI(docs_url="/")

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)