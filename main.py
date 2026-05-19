from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.userRoute import router as user_router
from database import engine, Base
from models.userModel import User

import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create the app
app = FastAPI(
    title="ExpenseTracker API",
    description="Python backend for ExpenseTracker application",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)

# Test route
@app.get("/")
def root():
    return {"message": "ExpenseTracker Backend Running Successfully"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Run server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)