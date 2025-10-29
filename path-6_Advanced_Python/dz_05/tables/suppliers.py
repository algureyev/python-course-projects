from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base_table import Base

class Suppliers(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, unique=True)  # ID продавца из Woysa Club (созданное)
    company_name = Column(String) # Название продавца из Woysa Club
    contact_person = Column(String)
    phone = Column(String)

    products = relationship("Products", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(company='{self.company_name}', contact='{self.contact_person}')>"