from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
from .core.config import settings

engine_kwargs = {"echo": True, "pool_pre_ping": True}

if settings.DB_TYPE == "mysql":
    DB_PASSWORD_ENCODED = urllib.parse.quote_plus(settings.DB_PASSWORD)
    DATABASE_URL = (
        f"mysql+pymysql://{settings.DB_USER}:{DB_PASSWORD_ENCODED}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
elif settings.DB_TYPE == "postgres":
    DB_PASSWORD_ENCODED = urllib.parse.quote_plus(settings.DB_PASSWORD)
    DATABASE_URL = (
        f"postgresql+psycopg2://{settings.DB_USER}:{DB_PASSWORD_ENCODED}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
else:
    raise ValueError(f"Unsupported DB_TYPE: {settings.DB_TYPE} - only 'mysql' and 'postgres' are supported.")

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()