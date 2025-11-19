from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user_model import User
from ..schemas.auth import LoginRequest, LoginResponse
from ..auth.jwt import create_access_token
from datetime import datetime
from fastapi import APIRouter
import logging
import bcrypt


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(login_request.email == User.email).first()

    if not user:
        raiseHttException("login failed, user does not exist")

    password_match = verify_passwords(login_request.password, user.password)

    if not password_match:
        raiseHttException("login failed, Invalid password")

    claims = {
        'sub': str(user.id),
        'email': user.email,
        'user_id': str(user.id)
    }

    try:
        access_token = create_access_token(claims)
    except Exception as e:
        raiseHttException(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return LoginResponse(
        access_token = access_token,
        token_type = 'bearer',
        email = user.email,
        user_id = user.id
    )


def verify_passwords(plain_text_password: str, hashed_password: str)-> bool:

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def raiseHttException(e, status = status.HTTP_401_UNAUTHORIZED):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status,
        detail = {
            "status": "error",
            "message": f"failed to create user {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )