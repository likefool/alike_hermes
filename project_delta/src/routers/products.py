from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import get_session
from models import Product, Category

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=List[Product])
def read_products(
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(None),
    limit: int = 10,
    offset: int = 0
) -> List[Product]:
    statement = select(Product)
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    
    # Sort by updated_at descending (newest first)
    statement = statement.order_by(Product.updated_at.desc())
    statement = statement.offset(offset).limit(limit)
    
    results = session.exec(statement).all()
    return list(results)

@router.get("/featured", response_model=List[Product])
def read_featured_products(
    session: Session = Depends(get_session),
    limit: int = 5
) -> List[Product]:
    statement = select(Product).where(Product.is_featured == True).order_by(Product.updated_at.desc())
    statement = statement.limit(limit)
    results = session.exec(statement).all()
    return list(results)

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
