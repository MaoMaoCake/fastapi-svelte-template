from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, DECIMAL, BLOB, Date, Boolean
from sqlalchemy.orm import declarative_base

from .utils import current_datetime, generate_salt

Base = declarative_base()


class BaseTXN(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=current_datetime())
    updated_at = Column(DateTime, nullable=False, default=current_datetime(), onupdate=current_datetime())
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)


class UserDB(BaseTXN):
    __tablename__ = "users"
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    salt = Column(String, nullable=False, default=generate_salt())

    profile_picture = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)