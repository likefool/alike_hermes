from fastapi import FastAPI
from database import init_db
from routers import products, categories

app = FastAPI(title="Project Delta E-commerce API")

# Register routers
app.include_router(categories.router)
app.include_router(products.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Welcome to Project Delta API. Use /docs for Swagger UI."}
