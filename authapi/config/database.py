import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

MYSQLUSER = os.getenv('MYSQLUSER')
MYSQLPORT = os.getenv('MYSQLPORT')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

TEST_URL_DATABASE =  f'mssql+pymssql://ekemainai:Beltaxboy@localhost:1444/dogehackertondb'

# Railway.app Cloud hosted
URL_DATABASE = f'mysql+pymysql://{MYSQLUSER}:{MYSQL_ROOT_PASSWORD}@viaduct.proxy.rlwy.net:{MYSQLPORT}/{MYSQL_DATABASE}'

# Local Cache Hosted
database_engine =  create_engine(
    url=TEST_URL_DATABASE,
    pool_timeout=40000.0,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autoflush=False, bind=database_engine)
Base = declarative_base()
