from fastapi import FastAPI

from app.routes.tables import router as tables_router
from app.routes.orders import router as orders_router

from app.routes.menu import router as menu_router

app = FastAPI(
    title="Restaurant Order Management API"
)
app.include_router(menu_router)

app.include_router(tables_router)
app.include_router(orders_router)

@app.get("/")
def home():
    return {
        "message": "Restaurant Order Management API is running"
    }
