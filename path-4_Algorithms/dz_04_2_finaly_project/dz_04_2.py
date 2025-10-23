import csv
import os
from typing import List, Dict, Any


class Product:
    """Класс для представления товара"""
    
    def __init__(self, product_id: int, name: str, category: str, 
                 price: float, weight: float, description: str):
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.weight = weight
        self.description = description
    
    def __str__(self):
        return (f"{self.name} | {self.category} | {self.price}₽ | "
                f"{self.weight}кг | {self.description}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует товар в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'weight': self.weight,
            'description': self.description
        }


class ProductManager:
    """Менеджер для работы с товарами"""
    
    def __init__(self, csv_file: str = 'products.csv'):
        self.csv_file = csv_file
        self.products = self.load_products()
    
    def load_products(self) -> List[Product]:
        """Загружает товары из CSV файла"""
        products = []
        if not os.path.exists(self.csv_file):
            print("❌ Файл с товарами не найден!")
            return products
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = Product(
                        product_id=int(row['Id']),
                        name=row['Название'],
                        category=row['Категория'],
                        price=float(row['Цена']),
                        weight=float(row['Вес']),
                        description=row['Описание']
                    )
                    products.append(product)
            print(f"✅ Загружено {len(products)} товаров")
        except Exception as e:
            print(f"❌ Ошибка при загрузке товаров: {e}")
        
        return products
    
    def display_products(self):
        """Отображает все товары"""
        if not self.products:
            print("❌ Нет товаров для отображения")
            return
            
        print("\n" + "="*80)
        print("🏪 КАТАЛОГ ТОВАРОВ СПОРТИВНОГО МАГАЗИНА")
        print("="*80)
        for product in self.products:
            print(f"{product.id:2d}. {product}")
        print("="*80)


class Cart:
    """Класс для работы с корзиной покупок"""
    
    def __init__(self):
        self.items: List[Product] = []
    
    def add_product(self, product: Product):
        """Добавляет товар в корзину"""
        self.items.append(product)
        print(f"✅ Товар '{product.name}' добавлен в корзину")
    
    def remove_product(self, product_id: int):
        """Удаляет товар из корзины по ID"""
        for i, product in enumerate(self.items):
            if product.id == product_id:
                removed_product = self.items.pop(i)
                print(f"✅ Товар '{removed_product.name}' удален из корзины")
                return True
        print(f"❌ Товар с ID {product_id} не найден в корзине")
        return False
    
    def display_cart(self):
        """Отображает содержимое корзины"""
        if not self.items:
            print("\n🛒 Корзина пуста")
            return
        
        print("\n" + "="*80)
        print("🛒 КОРЗИНА ПОКУПОК")
        print("="*80)
        total_price = 0
        total_weight = 0
        
        for i, product in enumerate(self.items, 1):
            print(f"{i:2d}. {product}")
            total_price += product.price
            total_weight += product.weight
        
        print("-"*80)
        print(f"Итого: {len(self.items)} товаров")
        print(f"Общая стоимость: {total_price:.2f}₽")
        print(f"Общий вес: {total_weight:.2f}кг")
        print("="*80)
    
    def get_total_price(self) -> float:
        """Возвращает общую стоимость товаров в корзине"""
        return sum(product.price for product in self.items)
    
    def clear(self):
        """Очищает корзину"""
        self.items.clear()
        print("✅ Корзина очищена")


class SortManager:
    """Менеджер для сортировки товаров в корзине"""
    
    @staticmethod
    def bubble_sort(items: List[Product], key: str, reverse: bool = False):
        """Пузырьковая сортировка"""
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if SortManager._compare(items[j], items[j + 1], key, reverse):
                    items[j], items[j + 1] = items[j + 1], items[j]
    
    @staticmethod
    def insertion_sort(items: List[Product], key: str, reverse: bool = False):
        """Сортировка вставками"""
        for i in range(1, len(items)):
            key_item = items[i]
            j = i - 1
            while j >= 0 and SortManager._compare(items[j], key_item, key, reverse):
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key_item
    
    @staticmethod
    def quick_sort(items: List[Product], key: str, reverse: bool = False):
        """Быстрая сортировка"""
        def _quick_sort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if SortManager._compare(x, pivot, key, not reverse)]
            middle = [x for x in arr if not SortManager._compare(x, pivot, key, not reverse) 
                     and not SortManager._compare(pivot, x, key, not reverse)]
            right = [x for x in arr if SortManager._compare(pivot, x, key, not reverse)]
            return _quick_sort(left) + middle + _quick_sort(right)
        
        sorted_items = _quick_sort(items)
        items.clear()
        items.extend(sorted_items)
    
    @staticmethod
    def merge_sort(items: List[Product], key: str, reverse: bool = False):
        """Сортировка слиянием"""
        def _merge_sort(arr):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = _merge_sort(arr[:mid])
            right = _merge_sort(arr[mid:])
            
            return SortManager._merge(left, right, key, reverse)
        
        sorted_items = _merge_sort(items)
        items.clear()
        items.extend(sorted_items)
    
    @staticmethod
    def _merge(left: List[Product], right: List[Product], key: str, reverse: bool):
        """Вспомогательная функция для слияния"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if SortManager._compare(left[i], right[j], key, reverse):
                result.append(right[j])
                j += 1
            else:
                result.append(left[i])
                i += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @staticmethod
    def _compare(product1: Product, product2: Product, key: str, reverse: bool) -> bool:
        """Сравнивает два товара по указанному ключу"""
        if key == 'price':
            value1, value2 = product1.price, product2.price
        elif key == 'weight':
            value1, value2 = product1.weight, product2.weight
        elif key == 'category':
            value1, value2 = product1.category, product2.category
        elif key == 'name':
            value1, value2 = product1.name, product2.name
        else:
            value1, value2 = product1.id, product2.id
        
        if reverse:
            return value1 < value2
        return value1 > value2


class ShopSimulator:
    """Основной класс симулятора магазина"""
    
    def __init__(self):
        self.product_manager = ProductManager()
        self.cart = Cart()
        self.sort_manager = SortManager()
    
    def display_menu(self):
        """Отображает главное меню"""
        print("\n" + "=" * 40)
        print("🏪 СИМУЛЯТОР СПОРТИВНОГО МАГАЗИНА")
        print("=" * 40)
        print("1. 📋 Показать каталог товаров")
        print("2. 🛒 Показать корзину")
        print("3. ➕ Добавить товар в корзину")
        print("4. ❌ Удалить товар из корзины")
        print("5. 🔄 Сортировать корзину")
        print("6. 🧹 Очистить корзину")
        print("7. 💰 Рассчитать итоговую стоимость")
        print("0. 🚪 Выход")
        print("=" * 40)
    
    def add_to_cart(self):
        """Добавляет товар в корзину"""
        if not self.product_manager.products:
            print("❌ Каталог товаров пуст")
            return
            
        self.product_manager.display_products()
        
        try:
            product_id = int(input("\nВведите ID товара для добавления в корзину: "))
            product = next((p for p in self.product_manager.products if p.id == product_id), None)
            
            if product:
                self.cart.add_product(product)
            else:
                print("❌ Товар с таким ID не найден")
        except ValueError:
            print("❌ Пожалуйста, введите корректный ID")
    
    def remove_from_cart(self):
        """Удаляет товар из корзины"""
        if not self.cart.items:
            print("❌ Корзина пуста")
            return
        
        self.cart.display_cart()
        
        try:
            product_id = int(input("\nВведите ID товара для удаления из корзины: "))
            self.cart.remove_product(product_id)
        except ValueError:
            print("❌ Пожалуйста, введите корректный ID")
    
    def sort_cart(self):
        """Сортирует корзину"""
        if not self.cart.items:
            print("❌ Корзина пуста")
            return
        
        print("\n" + "=" * 40)
        print("ВЫБОР АЛГОРИТМА СОРТИРОВКИ")
        print("=" * 40)
        print("1. Пузырьковая сортировка")
        print("2. Сортировка вставками")
        print("3. Быстрая сортировка")
        print("4. Сортировка слиянием")
        
        try:
            algo_choice = int(input("Выберите алгоритм сортировки (1-4): "))
            if algo_choice not in [1, 2, 3, 4]:
                print("❌ Неверный выбор алгоритма")
                return
        except ValueError:
            print("❌ Пожалуйста, введите число от 1 до 4")
            return
        
        print("\n" + "=" * 40)
        print("КРИТЕРИЙ СОРТИРОВКИ")
        print("=" * 40)
        print("1. По цене")
        print("2. По весу")
        print("3. По категории")
        print("4. По названию")
        
        try:
            key_choice = int(input("Выберите критерий сортировки (1-4): "))
            key_map = {1: 'price', 2: 'weight', 3: 'category', 4: 'name'}
            if key_choice not in key_map:
                print("❌ Неверный выбор критерия")
                return
            key = key_map[key_choice]
        except ValueError:
            print("❌ Пожалуйста, введите число от 1 до 4")
            return
        
        try:
            order = input("Сортировать по возрастанию? (да/нет): ").lower()
            reverse = order not in ['да', 'д', 'yes', 'y']
        except:
            reverse = False
        
        # Применяем выбранный алгоритм сортировки
        algo_map = {
            1: self.sort_manager.bubble_sort,
            2: self.sort_manager.insertion_sort,
            3: self.sort_manager.quick_sort,
            4: self.sort_manager.merge_sort
        }
        
        algorithm_names = ['Пузырьковую', 'Сортировку вставками', 'Быструю', 'Сортировку слиянием']
        print(f"\n🔄 Применяем {algorithm_names[algo_choice-1]} сортировку...")
        
        algo_map[algo_choice](self.cart.items, key, reverse)
        
        print("✅ Корзина отсортирована!")
        self.cart.display_cart()
    
    def calculate_total(self):
        """Рассчитывает итоговую стоимость"""
        if not self.cart.items:
            print("❌ Корзина пуста")
            return
        
        total = self.cart.get_total_price()
        print(f"\n💰 ИТОГОВАЯ СТОИМОСТЬ: {total:.2f}₽")
        
        # Учет скидок
        if total > 10000:
            discount = total * 0.1  # 10% скидка при покупке от 10000₽
            final_price = total - discount
            print(f"🎁 Скидка 10%: -{discount:.2f}₽")
            print(f"💵 К ОПЛАТЕ: {final_price:.2f}₽")
    
    def run(self):
        """Запускает главный цикл приложения"""
        print("🚀 Запуск симулятора магазина...")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nВыберите действие (0-7): ")
                
                if choice == '0':
                    print("👋 До свидания! Спасибо за покупки!")
                    break
                elif choice == '1':
                    self.product_manager.display_products()
                elif choice == '2':
                    self.cart.display_cart()
                elif choice == '3':
                    self.add_to_cart()
                elif choice == '4':
                    self.remove_from_cart()
                elif choice == '5':
                    self.sort_cart()
                elif choice == '6':
                    self.cart.clear()
                elif choice == '7':
                    self.calculate_total()
                else:
                    print("❌ Неверный выбор. Пожалуйста, выберите от 0 до 7")
            
            except KeyboardInterrupt:
                print("\n👋 Программа завершена пользователем")
                break
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    # Проверяем наличие файла с товарами
    if not os.path.exists('products.csv'):
        print("❌ Файл 'products.csv' не найден!")
        print("📝 Создайте его с помощью скрипта 'create_products.py'")
    else:
        app = ShopSimulator()
        app.run()