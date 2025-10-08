import random
import time

print("\n" + "=" * 60)
print("ЗАДАНИЕ 1")
print("=" * 60)

def fibonacci(n, depth = 0, call_stack = None):
    """
    Рекурсивная функция для вычисления n-го числа Фибоначчи.
    
    Args:
        n: номер числа Фибоначчи
        depth: глубина рекурсии (для анализа стека вызовов)
        call_stack: список для записи вызовов (для анализа)
        
    Returns:
        int: n-е число Фибоначчи
    """
    if call_stack is None:
        call_stack = []
    
    # Визуализация стека - для анализа
    indent = "  " * depth
    call_info = f"{indent}fib({n})"
    call_stack.append(call_info)
    print(f"{call_info}")
    
    # Базовые случаи
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    # Рекурсивный случай
    result = fibonacci(n - 1, depth + 1, call_stack) + fibonacci(n - 2, depth + 1, call_stack)
    
    # Визуализация стека - возврат значения
    return_info = f"{indent}return {result}"
    call_stack.append(return_info)
    print(f"{return_info}")
    
    return result

# Анализ функции и стека вызовов для n = 5
print(fibonacci(5))


# Задание 2
def find_max_recursive(arr):
    """
    Рекурсивная функция для нахождения максимального элемента в списке
    с использованием подхода "Разделяй и властвуй".
    
    Args:
        arr: список элементов
                
    Returns:
        Максимальный элемент в списке
    """
    start = 0
    end = len(arr) - 1

      
    # Базовый случай - один элемент
    if start == end:
        return arr[start]
    
    # Базовый случай - два элемента
    if end - start == 1:
        return arr[start] if arr[start] > arr[end] else arr[end]
    
    mid = (start + end) // 2
    
    # Находим максимум в левой и правой половинах
    left_max = find_max_recursive(arr[:mid])
    right_max = find_max_recursive(arr[mid + 1:])
    
    # Объединяем результаты
    return left_max if left_max > right_max else right_max

# Задание 3
def quicksort(arr):
    """
    Реализация быстрой сортировки (QuickSort).
    
    Args:
        arr: список для сортировки
        
    Returns:
        List[Any]: отсортированный список
    """
    # Базовый случай - пустой список или один элемент
    if len(arr) <= 1:
        return arr
    
    # Выбираем опорный элемент (pivot)
    pivot = arr[len(arr) // 2]
    
    # Разделяем на три списка
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Рекурсивно сортируем левую и правую части
    return quicksort(left) + middle + quicksort(right)

# для сравнения двух способо сортировки, добавляем функцию Сортировка вставки
def insertion_sort(arr):
    """
    Реализация сортировки вставками.
    
    Args:
        arr: список для сортировки
        
    Returns:
        List[Any]: отсортированный список
    """
    sorted_arr = arr.copy()
    
    for i in range(1, len(sorted_arr)):
        key = sorted_arr[i]
        j = i - 1
        
        while j >= 0 and sorted_arr[j] > key:
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        sorted_arr[j + 1] = key
    
    return sorted_arr



# Сравнение времени выполнения двух алгоритмов сортировки
print("\n" + "=" * 60)
print("ЗАДАНИЕ 3")
print("=" * 60)

# Создаем списки для тестирования
sizes = [10, 100, 1000]
list_for_test = []

for size in sizes:
    test_list = [random.randint(0, 1000) for _ in range(size)]
    list_for_test.append(test_list)


# Сравниваем различные алгоритмы на одном списке
times_quicksort = []
time_insertion = []

for list in list_for_test:
    start = time.time()
    result = quicksort(list)
    end = time.time()
    times_quicksort.append(end - start)
    start = time.time()
    result = insertion_sort(list)
    end = time.time()
    time_insertion.append(end - start)

# Вывод данных о тестировании

for i in range(len(sizes)):
    print(f"Количество элементов: {sizes[i]}. Время быстрой сортировки: {times_quicksort[i]}. Время сортировки вставкой: {time_insertion[i]}.")