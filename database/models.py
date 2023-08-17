from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import sqlalchemy as sql
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


Base: DeclarativeMeta = declarative_base()


class Paste(Base):
    __tablename__ = 'paste'

    id: Mapped[str] = mapped_column(
        sql.VARCHAR(8), primary_key=True
    )
    date_creation: Mapped[datetime] = mapped_column(
        sql.TIMESTAMP, nullable=False
    )
    date_delete: Mapped[datetime] = mapped_column(
        sql.TIMESTAMP, nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        sql.INTEGER, sql.ForeignKey('user.id'), nullable=True
    )
    author = relationship('User', back_populates='pastes')


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        sql.INTEGER, primary_key=True
    )   
    username: Mapped[str] = mapped_column(
        sql.String(length=50), nullable=False
    )
    email: Mapped[str] = mapped_column(
        sql.String(length=320), unique=True, index=True, nullable=False
    )
    date_registration: Mapped[datetime] = mapped_column(
        sql.TIMESTAMP, default=datetime.utcnow
    )
    hashed_password: Mapped[str] = mapped_column(
        sql.String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(sql.Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        sql.Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        sql.Boolean, default=False, nullable=False
    )
    pastes = relationship('Paste', back_populates='author')









