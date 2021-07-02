from sqlalchemy import Table, Column, Integer, Float, Boolean, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Basket(Base):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)

    active = Column(Boolean)
    weighting_method = Column(String) # TODO: Add a constraint for this
    weight = Column(Float)

    # TODO: Figure out what back_populates does
    stocks = relationship('Stock', back_populates='basket')

    
class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)

    symbol = Column(String, unique=True)

    basket = relationship('Basket', back_populates='stocks')
