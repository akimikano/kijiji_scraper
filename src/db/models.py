from sqlalchemy import String, Float, Date, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy import MetaData

Base = declarative_base()
Base.metadata = MetaData()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class Apartment(BaseModel):
    __tablename__ = 'apartments'

    name = Column(String)
    price = Column(Float)
    currency = Column(String(3))
    date = Column(Date)
    city = Column(String)
    img = Column(Text)
    description = Column(Text)
    beds = Column(String)

    def __repr__(self):
        return self.name
