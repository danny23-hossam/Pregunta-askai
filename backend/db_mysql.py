"""Relational database layer (MySQL via SQLAlchemy).

Stores user accounts. The integer primary key ``User.id`` is the link that the
MongoDB chat-history documents reference, so the two databases relate to each
other through this id.
"""
import os
import time

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

MYSQL_USER = os.getenv("MYSQL_USER", "pregunta")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "pregunta")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "pregunta")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=280)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def init_db(retries: int = 30, delay: float = 2.0) -> None:
    """Create tables, waiting for MySQL to accept connections first."""
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as err:  # MySQL not ready yet
            last_err = err
            time.sleep(delay)
    raise RuntimeError(f"MySQL not reachable after {retries} attempts: {last_err}")


def get_session():
    """FastAPI dependency yielding a scoped SQLAlchemy session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
