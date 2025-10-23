from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG
from connection import Connection
from base_table import Base
from tables.products import Products
from tables.orders import Orders
from tables.suppliers import Suppliers

def main():
    # Создание подключения с конфигом
    connection = Connection(**DB_CONFIG)
    
    # Создание движка и сессии
    engine = connection.engine
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Создание таблиц
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Таблицы созданы успешно!")
        
        # CRUD операции для Products (пример)
        
        # CREATE - Добавление данных
        product1 = Products(name="Ноутбук", price=50000.0, quantity=10)
        product2 = Products(name="Мышь", price=1500.0, quantity=25)
        session.add_all([product1, product2])
        session.commit()
        print("Товары добавлены")
        
        # READ - Чтение данных
        products = session.query(Products).all()
        print("Все товары:", products)
        
        expensive_products = session.query(Products).filter(Products.price > 1000).all()
        print("Дорогие товары:", expensive_products)
        
        # UPDATE - Обновление данных
        product = session.query(Products).filter_by(name="Мышь").first()
        if product:
            product.price = 1200.0
            session.commit()
            print("Цена мыши обновлена")
        
        # DELETE - Удаление данных
        product_to_delete = session.query(Products).filter_by(name="Ноутбук").first()
        if product_to_delete:
            session.delete(product_to_delete)
            session.commit()
            print("Ноутбук удален")
            
        # Проверка финального состояния
        final_products = session.query(Products).all()
        print("Финальный список товаров:", final_products)
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()