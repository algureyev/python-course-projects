from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG
from connection import Connection
from base_table import Base
from tables.products import Products
from tables.orders import Orders
from tables.suppliers import Suppliers
import asyncio
from async_loader import WoysaLoader

async def load_woysa_data(session):
    """Загрузка данных из Woysa и заполнение БД"""
    loader = WoysaLoader()
    categories = [10000, 15000, 20000, 21000]
    
    print("Начинаем загрузку данных с Woysa...")
    data_frame = await loader.get_data(categories, batch_size=2, max_workers=3)
    print(f"Получено {len(data_frame)} записей с Woysa")

    for _, row in data_frame.iterrows():
        # Создаем или находим продавца
        seller_name = row.get('Продавец', 'Unknown Seller')
        seller_id = hash(seller_name) % 1000000
        
        supplier = session.query(Suppliers).filter_by(seller_id=seller_id).first()
        if not supplier:
            supplier = Suppliers(
                seller_id=seller_id,
                company_name=seller_name,
                contact_person="Not specified", 
                phone="Not specified"
            )
            session.add(supplier)
            session.commit()

        # Создаем товар
        product = session.query(Products).filter_by(sku=row.get('SKU')).first()
        if not product:
            product = Products(
                sku=row.get('SKU'),
                name=row.get('Наименование', 'Unknown Product'),
                brand=row.get('Бренд', 'Unknown Brand'),
                category_name=row.get('Категория', 'Unknown Category'),
                price=row.get('Цена', 0.0),
                quantity=row.get('ПоследниеОстаткиНаскладах', 0),
                orders_count=row.get('Кол-воЗаказов', 0),
                supplier_id=supplier.id
            )
            session.add(product)
            session.commit()

        # Создаем заказ
        customer_name = f"Customer_{row.get('SKU')}"
        order = Orders(customer_name=customer_name, product_id=product.id)
        session.add(order)

    session.commit()
    print(f"База данных заполнена: создано {len(data_frame)} заказов")

def show_orders(session):
    """Показываем ПЕРВЫЕ 10 заказов с полными названиями через DTO"""
    orders = session.query(Orders).limit(10).all()
    print("\n" + "="*50)
    print("ПЕРВЫЕ 10 ЗАКАЗОВ (данные автоматически загружены из Woysa)")
    print("="*50)
    for i, order in enumerate(orders, 1):
        dto = order.to_dto()
        print(f"{i}. {dto}")

def show_products_with_suppliers(session):
    """Показываем ПЕРВЫЕ 10 товаров с информацией о продавцах"""
    products = session.query(Products).limit(10).all()
    print("\n" + "="*50)
    print("ПЕРВЫЕ 10 ТОВАРОВ С ИНФОРМАЦИЕЙ О ПРОДАВЦАХ")
    print("="*50)
    for i, product in enumerate(products, 1):
        print(f"{i}. Товар: {product.name}")
        print(f"   Бренд: {product.brand}")
        print(f"   Категория: {product.category_name}")
        print(f"   Цена: {product.price} руб.")
        print(f"   Остаток: {product.quantity} шт.")
        print(f"   Заказов: {product.orders_count}")
        print(f"   Продавец: {product.supplier.company_name}")
        print("-" * 30)

def main():
    """Основная функция - полностью автоматический процесс"""
    print("ЗАПУСК АВТОМАТИЧЕСКОЙ ЗАГРУЗКИ ДАННЫХ")
    print("="*50)
    
    connection = Connection(**DB_CONFIG)
    engine = connection.engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Создаем таблицы если не существуют
        # Base.metadata.drop_all(engine) # удаление старой структуры и последующе создание под данные Waosa Club - разовая акция
        Base.metadata.create_all(engine)
        print("✓ Таблицы БД созданы/проверены")

        # Проверяем, нужно ли загружать данные
        existing_orders = session.query(Orders).count()
        
        if existing_orders == 0:
            print("✓ Начинаем загрузку данных с Woysa...")
            asyncio.run(load_woysa_data(session))
            print("✓ Данные успешно загружены и сохранены в БД")
        else:
            print(f"✓ В базе уже есть {existing_orders} заказов")

        # Показываем результаты (первые 10 записей)
        show_orders(session)
        show_products_with_suppliers(session)

        # Показываем общую статистику
        total_orders = session.query(Orders).count()
        total_products = session.query(Products).count()
        total_suppliers = session.query(Suppliers).count()
        
        print("\n" + "="*50)
        print("ОБЩАЯ СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("="*50)
        print(f"Всего заказов в базе: {total_orders}")
        print(f"Всего товаров в базе: {total_products}")
        print(f"Всего поставщиков в базе: {total_suppliers}")
        print("="*50)

    except Exception as e:
        session.rollback()
        print(f"✗ Ошибка: {e}")
    finally:
        session.close()
        print("\n✓ Процесс завершен")

if __name__ == "__main__":
    main()