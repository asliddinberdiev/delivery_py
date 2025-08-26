import datetime

from fastapi import APIRouter, status, HTTPException, Depends
from starlette.responses import JSONResponse
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

from schemas import SignUpModel, SigninModel
from database import engine, session
from models import User

session = session(bind=engine)
access_lifetime = datetime.timedelta(minutes=60)
refresh_lifetime = datetime.timedelta(days=1)

auth_router = APIRouter(prefix="/auth", tags=["AUTH"])

@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, Authorize: AuthJWT = Depends()):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "This email already exists"
        )

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "This username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)


    access_token = Authorize.create_access_token(subject=new_user.username, expires_time=access_lifetime)
    refresh_token = Authorize.create_refresh_token(subject=new_user.username, expires_time=refresh_lifetime)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "refresh_token": refresh_token}
    )

@auth_router.post("/sign-in", status_code=status.HTTP_200_OK)
async def signin(user: SigninModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"access_token": access_token, "refresh_token": refresh_token}
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

@auth_router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        db_user = session.query(User).filter(
            or_(
                User.username == current_user,
                User.email == current_user
            )
        ).first()

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        new_access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)

        response_model = {
            'success': True,
            'code': 200,
            'message': 'Access token generated successfully',
            'data': {
                'access_token': new_access_token
            }
        }

        return response_model
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )