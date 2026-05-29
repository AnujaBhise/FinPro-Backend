

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# PostgreSQL Supabase Connection
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base
Base = declarative_base()


