import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(
            host=settings.db_host,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            cursor_factory=RealDictCursor
        )
        cursor=conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Connecting to database failed")
        print("Error:",e)
        time.sleep(2)