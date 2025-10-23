from sqlalchemy import Column, Integer, String, Float
from base_table import Base

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"