from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import List
from models import Category, Product
from database import create_db_and_tables, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/categories/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@app.get("/categories/", response_model=List[Category])
def read_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@app.post("/products/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products/", response_model=List[Product])
def read_products(category_id: int = Query(None), session: Session = Depends(get_session)):
    statement = select(Product)
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    return session.exec(statement).all()

@app.get("/products/featured/", response_model=List[Product])
def read_featured(session: Session = Depends(get_session)):
    statement = select(Product).where(Product.is_featured == True)
    return session.exec(statement).all()
