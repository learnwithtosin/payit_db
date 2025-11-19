from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
from app.database import engine, get_db
from sqlalchemy.orm import Session, defer
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..models.user_model import User
from ..middlewares.auth import AuthMiddleware
from fastapi import APIRouter
import bcrypt
import logging
import pymysql

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    return current_user


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter((User.email == user.email) | (User.phone == user.phone)).first()
    if user_exists:
        raise HTTPException(status_code=404, detail="User already exists!")
          
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salts)

    new_user = User(
        **user.dict(exclude={"password", "confirm_password", "gender", "category"}),
        password=hashed_password.decode(),
        gender = user.gender.value,
        category = user.category.value
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)

def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )

 

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).options(defer(User.password)).all()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_with_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exixts!")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_update = db.query(User).filter(User.id == user_id).first()
    if not user_update:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found!"
        )
    for field, value in user.dict().items():
        setattr(user_update, field, value)
    db.commit()
    db.refresh(user_update)
    return user_update

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exixts!")

    db.delete(db_user)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "User deleted sucessfully"
    )
    