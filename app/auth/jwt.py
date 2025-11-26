from jose import jwt, JWTError
import bcrypt
import os
from typing import Optional
from datetime import timedelta, datetime

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dd876043d55eebc302f01b3deeb99d8e5c3dceaf92675427c11067963fdefc55')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_TIME', 5))



def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None)-> str:
    try:
        if expires_delta:
            expiration_time = datetime.utcnow() + expires_delta
        else:
            expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

        claims.update({'exp': expiration_time})

        return jwt.encode(claims, SECRET_KEY, ALGORITHM)
    except JWTError as e:
        raise e

def verify_access_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, ALGORITHM)
        except JWTError as e:
            raise e


# def verify_password(plain_text_password: str, hashed_password: str)-> bool:
#     plain_text_password = plain_text_password.encode('utf-8')

#     return bcrypt.checkpw(plain_text_password, hashed_password)


# def verify_access_token(token: str):
#     try:
#         return jwt.decode(token, SECRET_KEY, ALGORITHM)
#     except JWTError as e:
#         raise e