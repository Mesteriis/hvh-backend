from config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.db_uri

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=settings.db_config.autocommit, autoflush=settings.db_config.autoflush, bind=engine
)

Base = declarative_base()
