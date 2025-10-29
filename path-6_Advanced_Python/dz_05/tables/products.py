from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from base_table import Base

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)  # Артикул из Woysa (SKU)
    name = Column(String)               # Наименование товара
    brand = Column(String)              # Бренд
    category_id = Column(Integer)       # ID категории из Woysa
    category_name = Column(String)      # Категория
    price = Column(Float)               # Цена
    quantity = Column(Integer)          # Последние остатки на складах
    orders_count = Column(Integer)  # Количество заказов
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))

    supplier = relationship("Suppliers", back_populates="products")
    orders = relationship("Orders", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"