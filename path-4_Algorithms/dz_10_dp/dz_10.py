# Задача 1

def knapsack(capacity, weights, values):
    """
    Решает задачу о рюкзаке методом динамического программирования.
    
    Args:
        capacity (int): Вместимость рюкзака
        weights (list): Список весов предметов
        values (list): Список стоимостей предметов
    
    Returns:
        int: Максимальная стоимость предметов, которые можно поместить в рюкзак
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]

# Тестирование задачи 1
capacity = 10
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]

result = knapsack(capacity, weights, values)
print(result)

# Задача 2

def lcs(str1, str2):
    """
    Находит длину наибольшей общей подпоследовательности (LCS) двух строк.
    
    Args:
        str1 (str): Первая строка
        str2 (str): Вторая строка
    
    Returns:
        int: Длина наибольшей общей подпоследовательности
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# Тестирование задачи 2
s1 = "ABCDGH"
s2 = "AEDFHR"

result = lcs(s1, s2)
print(result)


# Задача 3

def count_ways_to_sum(n):
    """
    Находит количество способов разбить число n на сумму положительных целых чисел.
    """
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    
    return dp[n]

# Тестирование задачи 3
n = 4
result = count_ways_to_sum(n)
print(result)

# Задача 4

def floyd_warshall(graph):
    """
    Находит кратчайшие пути между всеми парами вершин в графе.
    
    Args:
        graph (list): Матрица смежности графа
        
    Returns:
        list: Матрица кратчайших расстояний между всеми парами вершин
    """
    n = len(graph)
    dist = [row[:] for row in graph]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist