from fastapi import FastAPI, HTTPException, status, Depends, File, UploadFile, Form
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
from app.database import engine, get_db
from sqlalchemy.orm import Session, defer
from ..schemas.schemas_product import ProductCreate, ProductResponse
from ..models import products, user_model, farmers, buyers, product_category 
from ..middlewares.auth import AuthMiddleware
from fastapi import APIRouter
from uuid import uuid4
import logging
import pymysql
import os
import aiofiles
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["products"]
)
UPLOAD_DIR = "/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create(product_data: ProductCreate,
#             current_user = Depends( AuthMiddleware), 
#            db: Session = Depends(get_db)):
#     new_farmer = db.query(farmers.Farmer).filter(farmers.Farmer.user_id == current_user.id).first()
#     if not new_farmer:
#         new_farmer = farmers.Farmer(user_id=current_user.id)
#         db.add(new_farmer)
#         db.commit()
#         db.refresh(new_farmer)

#     new_category = db.query(product_category.ProductCategory).filter(product_category.ProductCategory.category_name == product_data.category.value).first()
#     if not new_category:
#         new_category = product_category.ProductCategory(category_name=product_data.category.value)
#         db.add(new_category)
#         db.commit()
#         db.refresh(new_category)

#     new_product = products.Product(
#         **product_data.model_dump(exclude={"category"}),
#         farmer_id  =  current_user.id,
#         category_id = new_category.id,
#         created_at = datetime.now(),
#         updated_at = datetime.now()
#     )
#     try:
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)
#         return new_product
#     except pymysql.DatabaseError as e:
#         raiseError(e, status.HTTP_500_INTERNAL_SERVER_ERROR)
#     print(new_product)
#     # print(product_data.__dict__)
#     # print(current_user.__dict__)

# def raiseError(e, status_code):
#     logger.error(f"failed to create record error: {e}")
#     raise HTTPException(
#         status_code=status_code,
#         detail = {
#             "status": "error",
#             "message": f"failed to create user: {e}",
#             "timestamp": f"{datetime.utcnow()}"
#         }
#     )



@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_product(farmer_id: int= Form(...),
                   category_id: int = Form(...),
                   image: UploadFile = File(...),
                   name: str = Form(...),
                   unit_price : float = Form(...),
                   quantity: int = Form(...),
                   current_user = Depends(AuthMiddleware),
                   db: Session = Depends(get_db)
                   ):
   


    allowed_extens = ["jpeg", "png", "jpg"]

    file_exten = image.filename.split(".")[-1].lower()

    if not file_exten in allowed_extens:
        raiseError("Invalid file extension")
    try:
        print("====================================")
        file_name = f"{uuid4()}.{file_exten}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as outputfile:
            content = await image.read()
            await outputfile.write(content)

    except Exception as e:
        raiseError("This is an internal server error!")

    



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


# @router.post("/products")
# def create_product(product: ProductCreate, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
#     user = db.query(user_model.User).filter(user_model.User.id == current_user.id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # if db.query(Product).filter(Product.email == product.email).first():
#     #     raise HTTPException(status_code=404, detail="Product already exists!")

#     new_farmer = db.query(farmers.Farmer).filter(farmers.Farmer.user_id == current_user.id).first()
#     if not new_farmer:
#         new_farmer = farmers.Farmer(user_id=current_user.id)
#         db.add(new_farmer)
#         db.commit()
#         db.refresh(new_farmer)
    
#     new_category = db.query(product_category.ProductCategory).filter(product_category.ProductCategory.category_name == product.category.value).first()
#     if not new_category:
#         new_category = product_category.ProductCategory(category_name=product.category.value)
#         db.add(new_category)
#         db.commit()
#         db.refresh(new_category)

          
#     new_product = products.Product(
#         **product.model_dump(exclude={"category"}),
#         farmer_id = new_farmer.id,
#         category_id = new_category.id,
#         created_at = datetime.now(),
#         updated_at = datetime.now(),

#     )
    

#     try:  
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)

#         return new_product
#     except pymysql.DataError as e:
#         raiseError(e)
#     except Exception as e:
#         raiseError(e)

# def raiseError(e):
#     logger.error(f"failed to create record error: {e}")
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail = {
#             "status": "error",
#             "message": f"failed to create product: {e}",
#             "timestamp": f"{datetime.utcnow()}"
#         }
#     )

@router.get("/products") #response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(products.Product).all()

@router.get("/products/{product_id}") #response_model=ProductResponse)
def get_product_by_product_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(products.Product).filter(products.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product with id entered does not exists!")
    return product

@router.get("/farmers/products/{farmer_id}")
def get_product_by_farmer_id(farmer_id: int, db: Session = Depends(get_db)):
    return db.query(products.Product).filter(products.Product.farmer_id == farmer_id).all()
    # if not farmer:
    #     raise HTTPException(status_code=404, detail="Farmer with id entered does not exists!")
    # return farmer


@router.put("/products/{product_id}") #response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    user = db.query(products.Product).filter(products.Product.farmer_id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Farmer with ID not found"
        )

    product_update = db.query(products.Product).filter(products.Product.id == product_id).first()
    if not product_update:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product not found!"
        )
    for field, value in product.dict().items():
        setattr(product_update, field, value)

    db_category = db.query(product_category.ProductCategory).filter(product_category.ProductCategory.category_name == product_update.category.value).first()
    if not db_category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found"
        )

    setattr(product_update, "category_id", db_category.id)



    db.commit()
    db.refresh(product_update)
    return product_update



@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(products.Product).filter(products.Product.farmer_id == current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail = "Farmer with ID not found")

    db_product = db.query(products.Product).filter(products.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product does not exixts!")

    db.delete(db_product)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Product deleted sucessfully"
    )