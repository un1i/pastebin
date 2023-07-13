from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import sqlalchemy as sql


Base: DeclarativeMeta = declarative_base()


class Paste(Base):
    __tablename__ = 'paste'
    id = sql.Column(sql.VARCHAR(8), primary_key=True)
    url = sql.Column(sql.TEXT, nullable=False)
    date_creation = sql.Column(sql.TIMESTAMP, nullable=False)
    date_delete = sql.Column(sql.TIMESTAMP, nullable=False)









