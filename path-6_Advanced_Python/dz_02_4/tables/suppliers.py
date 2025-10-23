from sqlalchemy import Column, Integer, String
from base_table import Base

class Suppliers(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    contact_person = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f"<Supplier(company='{self.company_name}', contact='{self.contact_person}')>"