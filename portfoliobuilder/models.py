from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Basket(Base):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)

    active = Column(Boolean)
    weighting_method = Column(String) # TODO: Add a constraint for this
    weight = Column(Float)

    stocks = relationship('Stock', cascade='all, delete')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    basket_id = Column(Integer, ForeignKey('basket.id'))

    symbol = Column(String, unique=True)

