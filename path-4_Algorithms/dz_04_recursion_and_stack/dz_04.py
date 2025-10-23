# Первое задание

def factorial(n):
    """
    Рекурсивная функция для вычисления факториала числа n.
    
    Args:
        n (int): число для вычисления факториала
        
    Returns:
        int: факториал числа n
        
    Raises:
        ValueError: если n отрицательное число
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    # Базовый случай
    if n == 0 or n == 1:
        return 1
    # Рекурсивный случай
    return n * factorial(n - 1)

# Второе задание
def recursive_sum(arr):
    """
    Рекурсивная функция для вычисления суммы всех элементов в списке.
    
    Args:
        arr (list): список чисел
        
    Returns:
        int/float: сумма всех элементов списка
    """
    # Базовый случай - пустой список
    if len(arr) == 0:
        return 0
    # Базовый случай - один элемент
    if len(arr) == 1:
        return arr[0]
    # Рекурсивный случай - сумма первого элемента и суммы остальных
    return arr[0] + recursive_sum(arr[1:])

# Третье задание
def recursive_binary_search(arr, target, left=0, right=None):
    """
    Рекурсивная функция для выполнения бинарного поиска в отсортированном списке.
    
    Args:
        arr (list): отсортированный список элементов
        target: элемент для поиска
        left (int): левая граница поиска
        right (int): правая граница поиска
        
    Returns:
        int: индекс найденного элемента или -1 если элемент не найден
    """
    # Инициализация правой границы при первом вызове
    if right is None:
        right = len(arr) - 1
    
    # Базовый случай - элемент не найден
    if left > right:
        return -1
    
    # Вычисление середины
    mid = (left + right) // 2
    
    # Базовый случай - элемент найден
    if arr[mid] == target:
        return mid
    # Рекурсивный случай - искать в правой половине
    elif arr[mid] < target:
        return recursive_binary_search(arr, target, mid + 1, right)
    # Рекурсивный случай - искать в левой половине
    else:
        return recursive_binary_search(arr, target, left, mid - 1)
    
# Четвертое задание
class Stack:
    """
    Класс Stack реализует структуру данных стек.
    
    Стек работает по принципу LIFO (Last In, First Out) - 
    последний пришел, первый ушел.
    """
    
    def __init__(self):
        """Инициализация пустого стека."""
        self.items = []
    
    def push(self, item):
        """
        Добавляет элемент на вершину стека.
        
        Args:
            item: элемент для добавления в стек
        """
        self.items.append(item)
    
    def pop(self):
        """
        Удаляет и возвращает элемент с вершины стека.
        
        Returns:
            Элемент с вершины стека
            
        Raises:
            IndexError: если стек пуст
        """
        if self.is_empty():
            raise IndexError("Попытка извлечения из пустого стека")
        return self.items.pop()
    
    def peek(self):
        """
        Возвращает элемент с вершины стека без его удаления.
        
        Returns:
            Элемент с вершины стека или None если стек пуст
        """
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self):
        """
        Проверяет, пуст ли стек.
        
        Returns:
            bool: True если стек пуст, False в противном случае
        """
        return len(self.items) == 0
    
    def size(self):
        """
        Возвращает количество элементов в стеке.
        
        Returns:
            int: количество элементов в стеке
        """
        return len(self.items)
    
    def __str__(self):
        """
        Возвращает строковое представление стека.
        
        Returns:
            str: строковое представление стека
        """
        return f"Stack({self.items})"

