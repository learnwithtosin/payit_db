from fastapi import FastAPI, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User
from schemas.auth import LoginRequest, LoginResponse
from auth.jwt import create_access_token
from fastapi.responses import RedirectResponse
from config.oauth import oauth
from models.enums import GenderEnum
from datetime import datetime
from config.oauth import AUTH0_DOMAIN, AUTH0_CLIENT_ID
from fastapi import APIRouter
import logging
import bcrypt
import pymysql


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/oauth",
    tags=["Oauth"]
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    try:
        return await oauth.auth0.authorize_redirect(request, redirect_uri = redirect_uri)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth Error: Failed to Authenticate User {e}"
        )

@router.get("/callback", name="callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        print("User token", token)
        user_info = token.get("userinfo")
        user = db.query(User).filter((user_info["email"] == User.email)).first()

   

        if not user:
            user = User(
                name = user_info["name"],
                phone = 12345678900,
                email = user_info["email"],
                password = "James1",
                gender = "M",
                location = "Jos"

            )

            db.add(user)
            db.commit()
            db.refresh(user)
        jwt = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "user_id": str(user.id)
            }
         )

        return {
            "access_token": jwt,
            "email": user.email,
            "id": user.id
        }


    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth Error: Failed to generate token {e}"
        )

    except pymysql.DataError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DB Error: {e}"
        )

@router.get("/logout")
def logout(request: Request):
    return_url = "http://localhost:8000"

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"returnTo={return_url}"
    )

    return RedirectResponse(url = logout_url)