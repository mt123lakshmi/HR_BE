from fastapi import FastAPI

from app.database.database import engine
from app.models import models
from app.routes import admin_routes
from app.routes import employee_routes
from app.routes import leave_routes
from app.routes import attendance_routes
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ameya HR Management")

app.include_router(admin_routes.router)
app.include_router(employee_routes.router)
app.include_router(leave_routes.router)
app.include_router(attendance_routes.router)
@app.get("/")
def root():
    return {"message": "API Running"}