from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:qwerty12345@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

)


# the engine is whats responsible for sqlalchemy to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionmaker allows us  to communicate with a database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All the models to create our table is extending the base class
Base = declarative_base()

# This is a dependency that is responsible for communicating with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()