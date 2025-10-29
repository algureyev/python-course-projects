from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base_table import Base
from datetime import datetime
from order_dto import OrderDTO

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_date = Column(DateTime, default=datetime.now)

    product = relationship("Products", back_populates="orders")

    def __repr__(self):
        return f"<Order(customer='{self.customer_name}', product_id={self.product_id})>"
    
    def to_dto(self) -> OrderDTO:
        return OrderDTO(
            order_id=self.id,
            customer_name=self.customer_name,
            product_name=self.product.name if self.product else "Unknown",
            company_name=self.product.supplier.company_name if self.product and self.product.supplier else "Unknown",
            order_date=self.order_date
        )