import random
import time
import matplotlib.pyplot as plt


def binary_search(sorted_list, target):
    """
    Реализация алгоритма бинарного поиска.
    
    Args:
        sorted_list: отсортированный список элементов
        target: элемент для поиска
    
    Returns:
        int: индекс элемента или -1 если элемент не найден
    """
    left = 0
    right = len(sorted_list) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Создаем список для тестирования
sorted_list = sorted([random.randint(1, 1000) for _ in range(100)])
print(sorted_list[:10])


# Тестируем функцию на случайных числах

element = [10, 150, 999]

for i in range(0, len(element)):
    start = time.time() 
    result = binary_search(sorted_list, element[i])
    end = time.time()
    print(f"Результат {result}. Время поиска: {end - start} сек")


# Сравнение бинарного и линейного поиска

# Функция линейного поиска из прошлого ДЗ
def linear_search(list_for_search: list, element: int) -> int:
    """Функция для поиска элемента в списке
    Args: 
        list_for_search - список, который принимает функция для анализа
        element - искомый элемент

    Returns:
        Индекс искомого элемента или -1 если элемент не найдет
    """
    try:
        for index, value in enumerate(list_for_search):
            if value == element:
                return index
        return -1
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return -1


binary_time = []
linear_time = []
target = 157

start = time.time()
binary_result = binary_search(sorted_list, target)
end = time.time()
binary_time = end - start

start = time.time()
linear_result = linear_search(sorted_list, target)
end = time.time()
linear_time = end - start

print(f"Бинарный поиск: {binary_time:.8f} сек (индекс: {binary_result})")
print(f"Линейный поиск: {linear_time:.8f} сек (индекс: {linear_result})")

# Построение графика
try:
    plt.figure(figsize=(10, 6))

    # Данные для графика
    algorithms = ['Бинарный поиск', 'Линейный поиск']
    times = [binary_time, linear_time]
    colors = ['blue', 'red']

    # Создаем столбчатую диаграмму
    bars = plt.bar(algorithms, times, color=colors, alpha=0.7)

    # Добавляем значения на столбцы
    for bar, time_val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.000001, 
                 f'{time_val:.8f} сек', ha='center', va='bottom')

    plt.xlabel('Алгоритмы поиска')
    plt.ylabel('Время выполнения (секунды)')
    plt.title(f'Сравнение времени поиска элемента {target}\n(Размер списка: {len(sorted_list)} элементов)')
    plt.grid(True, alpha=0.3)

    # Сохраняем график
    plt.savefig('binary_search_performance.png', dpi=300, bbox_inches='tight')
    print("График успешно сохранен как 'binary_search_performance.png'")
    
    # Показываем график
    plt.show()
except Exception as e:
    print(f"Ошибка при создании графика: {e}")