import random
import time
import matplotlib.pyplot as plt


def bubble_sort(arr):
    """
    Реализация алгоритма сортировки пузырьком.
    
    Args:
        arr: список для сортировки
    
    Returns:
        list: отсортированный список
    """
    n = len(arr)
    # Создаем копию списка чтобы не изменять оригинал
    sorted_arr = arr.copy()
    
    for i in range(n):
        # Флаг для оптимизации - если не было обменов, список отсортирован
        swapped = False
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        # Если не было обменов, выходим досрочно
        if not swapped:
            break
    return sorted_arr


def selection_sort(arr):
    """
    Реализация алгоритма сортировки выбором.
    
    Args:
        arr: список для сортировки
    
    Returns:
        list: отсортированный список
    """
    n = len(arr)
    sorted_arr = arr.copy()
    
    for i in range(n):
        # Находим минимальный элемент в оставшейся части
        min_idx = i
        for j in range(i + 1, n):
            if sorted_arr[j] < sorted_arr[min_idx]:
                min_idx = j
        
        # Меняем найденный минимальный элемент с первым элементом
        sorted_arr[i], sorted_arr[min_idx] = sorted_arr[min_idx], sorted_arr[i]
    
    return sorted_arr


def insertion_sort(arr):
    """
    Реализация алгоритма сортировки вставками.
    
    Args:
        arr: список для сортировки
    
    Returns:
        list: отсортированный список
    """
    sorted_arr = arr.copy()
    
    for i in range(1, len(sorted_arr)):
        key = sorted_arr[i]
        j = i - 1
        
        # Перемещаем элементы arr[0..i-1], которые больше key,
        # на одну позицию вперед
        while j >= 0 and sorted_arr[j] > key:
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        sorted_arr[j + 1] = key
    
    return sorted_arr


# Создаем список для тестирования
list = [random.randint(1, 1000) for _ in range(100)]
print(list[:20])

# Сравниваем различные алгоритмы на одном списке

start = time.time()
bubble_sort_result = bubble_sort(list)
end = time.time()
#print(bubble_sort_result[:20])
bubble_sort_time = end - start

start = time.time()
selection_sort_result = selection_sort(list)
end = time.time()
#print(selection_sort_result[:20])
selection_sort_time = end - start

start = time.time()
insertion_sort_result = bubble_sort(list)
end = time.time()
#print(insertion_sort_result[:20])
insertion_sort_time = end - start

print(f"Сортировка пузырьком: {bubble_sort_time:.8f} сек (часть списка: {bubble_sort_result[:20]}")
print(f"Сортировка выбором: {selection_sort_time:.8f} сек (часть списка: {selection_sort_result[:20]}")
print(f"Сортировка вставками: {insertion_sort_time:.8f} сек (часть списка: {insertion_sort_result[:20]}")

# Построение графика
try:
    plt.figure(figsize=(10, 6))

    # Данные для графика
    algorithms = ['Сортировка пузырьком', 'Сортировка выбором', 'Сортировка вставками']
    times = [bubble_sort_time, selection_sort_time, insertion_sort_time]
    colors = ['blue', 'red', 'green']

    # Создаем столбчатую диаграмму
    bars = plt.bar(algorithms, times, color=colors, alpha=0.7)

    # Добавляем значения на столбцы
    for bar, time_val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.000001, 
                 f'{time_val:.8f} сек', ha='center', va='bottom')

    plt.xlabel('Алгоритмы поиска')
    plt.ylabel('Время выполнения (секунды)')
    plt.title(f'Сравнение времени сортировки различными алгоритмами')
    plt.grid(True, alpha=0.3)

    # Сохраняем график
    plt.savefig('simple_sorting.png', dpi=300, bbox_inches='tight')
        
    # Показываем график
    plt.show()
except Exception as e:
    print(f"Ошибка при создании графика: {e}")