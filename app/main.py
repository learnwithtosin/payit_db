from fastapi import FastAPI
from .database import engine
from .models.base import Base
from app.routes import user, products
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PayIt App",
    version="0.0.1",
    description="market place..."
)


def db_and_table_init():
    retries = 30
    for i in range(retries):
        try:
            logger.info("Initializing database...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialization successful.")
            break
        except Exception as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries})...")
            logger.error(f"Error: {e}")
            time.sleep(3)


@app.on_event("startup")
def on_startup():
    db_and_table_init()



app.include_router(user.router)
app.include_router(products.router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hello world"
    }






# from fastapi import FastAPI, status, HTTPException
# #from app.models.base import Base
# from .database import engine
# from .models.base import Base
# from app.models.user_model import User
# from app.routes import user
# import time
# from app.models import user_model
# # from datetime import datetime
# # from typing import List, Optional, Dict
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Base.metadata.create_all(bind=engine)


# def db_and_table_init():
#     retries = 30
#     for i in range(retries):
#         try:
#             logger.info("STARTING APPLICATION!")
#             Base.metadata.create_all(bind=engine)
#             logger.info("STARTING APPLICATION!")
#             break
#         except Exception as e:
#             logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries})...")
#             logger.info(f"DATABASE INITIALIZATION FAILED: {e}")

#             time.sleep(3)
#         except Exception as e:
#             logger.info(f"DATABASE INITIALIZATION FAILED: {e}")

# app = FastAPI(
#     title = "PayIt App",
#     version = "0.0.1",
#     description = "market place..."
#     )

# app.include_router(user_model.router)
# @app.on_event("startup")
# def on_startup():
#     db_and_table_init()

# @app.get("/")
# def home():
#     return {
#         "status": "success",
#         "message": "Hello world"
#     }

