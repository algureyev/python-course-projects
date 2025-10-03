import random
import time
import matplotlib.pyplot as plt

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

# Создание случайного списка из 100 значений и поиских нескольких элементов

random_list = [random.randint(0, 1000) for _ in range (100)]
element = [10, 150, 999]

for i in range(0, len(element)):
    start = time.time() 
    result = linear_search(random_list, element)
    end = time.time()
    print(f"Результат {result}. Время поиска: {end - start} сек")



# Сравнение времени 10, 100 и 1000 элементов и построение графика

element = 777
sizes = [10, 100, 1000]
times = []

for size in sizes:
    test_list = [random.randint(0, 1000) for _ in range(size)]

    start = time.time() 
    result = linear_search(test_list, element)
    end = time.time()
    execution_time = end - start
    
    times.append(execution_time)

plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Размер списка')
plt.ylabel('Время выполнения (сек)')
plt.title('Зависимость времени линейного поиска от размера списка')
plt.grid(True, alpha=0.3)
plt.xscale('log')  # логарифмическая шкала для лучшего отображения
plt.yscale('log')
plt.savefig('linear_search_performance.png')  # сохраняем график
plt.show()
