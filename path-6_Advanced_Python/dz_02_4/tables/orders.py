from sqlalchemy import Column, Integer, String, DateTime
from base_table import Base
from datetime import datetime

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    product_id = Column(Integer)
    order_date = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Order(customer='{self.customer_name}', product_id={self.product_id})>"