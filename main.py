from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routers.userRoute import router as user_router
from routers.incomeRoute import router as income_router
from routers.dashboardRoute import router as dashboard_router
from routers.expenseRoute import router as expense_router
from database import engine, Base

from models.userModel import User
from models.incomeModel import Income

import uvicorn


# Create database tables
Base.metadata.create_all(bind=engine)


# Create app
app = FastAPI(
    title="Finance Tracking API",
    description="Python backend for Finpro - Finance tracking application",
    version="1.0.0"
)


# Redirect root to /docs
@app.get("/")
def root():
    return RedirectResponse(url="/docs")


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(user_router)
app.include_router(income_router)
app.include_router(dashboard_router)
app.include_router(expense_router)

# Run server
if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )