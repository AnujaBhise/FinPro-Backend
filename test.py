from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres.waqvawwslnfakrjtvsll:FinProDatabase@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres?sslmode=require"

engine = create_engine(DATABASE_URL)

try:
    conn = engine.connect()
    print("Connected Successfully!")
    conn.close()
except Exception as e:
    print(e)