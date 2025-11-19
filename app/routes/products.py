from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
from app.database import engine, get_db
from sqlalchemy.orm import Session, defer
from ..schemas.schemas_product import ProductCreate, ProductResponse, ProductUpdate
from ..models.products import Product
from ..models.user_model import User
from fastapi import APIRouter
import logging
import pymysql



router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/products", response_model=ProductResponse)
def create_product(users_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == users_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if db.query(Product).filter(Product.email == product.email).first():
    #     raise HTTPException(status_code=404, detail="Product already exists!")

          
    new_product = Product(
        **product.model_dump(),
        created_at = datetime.now(),
        updated_at = datetime.now(),
        user_id = users_id
    )
    

    try:  
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
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
            "message": f"failed to create product: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )

@router.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_product_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product with id entered does not exists!")
    return product

@router.get("/products/{user_id}", response_model=ProductResponse)
def get_product_by_user_id(user_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.user_id == user_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product with user_id entered does not exists!")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    product_update = db.query(Product).filter(Product.user_id == user_id).first()
    if not product_update:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product not found!"
        )
    for field, value in product.dict().items():
        setattr(product_update, field, value)
    db.commit()
    db.refresh(product_update)
    return product_update

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product does not exixts!")

    db.delete(db_product)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Product deleted sucessfully"
    )