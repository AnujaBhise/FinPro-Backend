from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQL Server Connection
SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://@DESKTOP-3QGTICG\\MSSQLSERVER01/ExpenseTracker?"
    "driver=ODBC+Driver+17+for+SQL+Server&"
    "trusted_connection=yes"
)

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