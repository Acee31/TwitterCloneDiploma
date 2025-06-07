"""This module contains the Base model for all tables in the database."""

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models."""


class BaseModel(Base):
    """Base model for all tables in the database."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())
