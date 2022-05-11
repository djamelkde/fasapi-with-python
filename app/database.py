from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings



#envar:
#   #DB_PASSWORD
#   #DB_USERNAME
#   #DB_NAME
#   #DB_URL

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>:<port_number>/<database_name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:esiINIdjMI21@localhost:5433/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#connection to the database
while True:
    try:
        conn = psycopg2.connect(host={settings.database_hostname}, database={settings.database_name}, user={settings.database_username}, 
                                port={settings.database_port}, password={settings.database_password}, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successfull :)")
        break
    except Exception as error:
        print("Connection to databse failed :(")
        print("error: ", error)
        time.sleep(2)

