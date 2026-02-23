from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer,
                primary_key=True,
                index=True)
    name = Column(String,
                  nullable=False)
    cnpj = Column (String,
                   unique=True,
                   nullable=False)
    plan = Column (String,
                   default = "free")