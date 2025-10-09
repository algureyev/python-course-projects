import random
import time

# Создание класса

class Queue:
    """
    Класс Queue реализует структуру данных очередь.
    
    Очередь работает по принципу FIFO (First In, First Out) - 
    первый пришел, первый ушел.
    """
    
    def __init__(self):
        """Инициализация пустой очереди."""
        self.items = []
    
    def enqueue(self, item):
        """
        Добавляет элемент в конец очереди.
        
        Args:
            item: элемент для добавления в очередь
        """
        self.items.append(item)
    
    def dequeue(self):
        """
        Удаляет и возвращает элемент из начала очереди.
        
        Returns:
            Элемент из начала очереди
            
        Raises:
            IndexError: если очередь пуста
        """
        if self.is_empty():
            raise IndexError("Попытка извлечения из пустой очереди")
        return self.items.pop(0)
    
    def peek(self):
        """
        Возвращает элемент из начала очереди без его удаления.
        
        Returns:
            Элемент из начала очереди или None если очередь пуста
        """
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self) -> bool:
        """
        Проверяет, пуста ли очередь.
        
        Returns:
            bool: True если очередь пуста, False в противном случае
        """
        return len(self.items) == 0

# Моделирование работы созданного класса на тестовом примере    
test_list = [["Задача 1", 5], ["Задача 2", 3], ["Задача 3", 7]]

queue_test = Queue()
current_time = 0

# Добавление задач в очередь
for task in test_list:
    queue_test.enqueue(task)

print(queue_test)

# Выполнение задач
while not queue_test.is_empty():
    task = queue_test.dequeue()
    task_name, duration = task
    print(f"Начало: {task_name}. Длительность задачи: {duration}сек")
    current_time += duration
    print(f"Завершено: {task_name} Время заверщения от запуска всей очереди: {current_time}сек")


# Сортировка слиянием

def merge_sort(arr):
    """
    Реализация сортировки слиянием merge.
    
    Args:
        arr: список для сортировки
        
    Returns:
        list: отсортированный список
    """
    def merge(left, right):
        """Внутренняя функция для слияния."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # Базовый случай
    if len(arr) <= 1:
        return arr
    
    # Разделяем и рекурсивно сортируем
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Объединяем отсортированные половины
    return merge(left_half, right_half)

# Реализация сортировки пузырьком для сравнения

def bubble_sort(arr) :
    """
    Реализация сортировки пузырьком для сравнения.
    
    Args:
        arr: список для сортировки
        
    Returns:
        List[Any]: отсортированный список
    """
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        if not swapped:
            break
    
    return sorted_arr

# Сравнение времени выполнения двух алгоритмов сортировки


# Создаем списки для тестирования
sizes = [10, 100, 1000]
list_for_test = []

for size in sizes:
    test_list = [random.randint(0, 1000) for _ in range(size)]
    list_for_test.append(test_list)


# Сравниваем различные алгоритмы на одном списке
times_merge_sort = []
time_bubble_sort = []

for list in list_for_test:
    # сортировка слиянием
    start = time.time()
    result = merge_sort(list)
    end = time.time()
    times_merge_sort.append(end - start)
    # пузырьковая сортировка
    start = time.time()
    result = bubble_sort(list)
    end = time.time()
    time_bubble_sort.append(end - start)

# Вывод данных о тестировании

for i in range(len(sizes)):
    print(f"Количество элементов: {sizes[i]}. Время сортировки слиянием: {times_merge_sort[i]}. Время пузырьковой сортировки: {time_bubble_sort[i]}.")