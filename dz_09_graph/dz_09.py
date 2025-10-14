class DirectedGraph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, from_vertex, to_vertex):
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list:
            self.adjacency_list[from_vertex].append(to_vertex)
        else:
            raise ValueError("Обе вершины должны существовать в графе")
    
    def bfs(self, start_vertex):
        if start_vertex not in self.adjacency_list:
            raise ValueError("Вершина не найдена в графе")
        
        visited = set()
        queue = [start_vertex]  # используем простой список как очередь
        result = []
        
        while queue:
            # Извлекаем первый элемент (эмуляция deque.popleft())
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Добавляем всех соседей в конец очереди
                for neighbor in self.adjacency_list[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def create_adjacency_matrix_from_edges(self):
        """Создает матрицу смежности на основе текущей структуры графа"""
        vertices = sorted(self.adjacency_list.keys())
        n = len(vertices)
        vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
        
        matrix = [[0] * n for _ in range(n)]
        
        for from_vertex, neighbors in self.adjacency_list.items():
            i = vertex_index[from_vertex]
            for to_vertex in neighbors:
                j = vertex_index[to_vertex]
                matrix[i][j] = 1
        
        return matrix, vertices
    
    def add_to_adjacency_matrix(self, matrix, vertices, new_vertex=None, new_edge=None):
        """
        Добавляет вершину или ребро в существующую матрицу смежности
        
        Args:
            matrix: текущая матрица смежности
            vertices: список вершин
            new_vertex: новая вершина для добавления (опционально)
            new_edge: кортеж (from_vertex, to_vertex) для нового ребра (опционально)
        """
        updated_matrix = [row[:] for row in matrix]
        updated_vertices = vertices[:]
        
        if new_vertex and new_vertex not in updated_vertices:
            updated_vertices.append(new_vertex)
            n = len(updated_vertices)
            
            for i in range(n - 1):
                updated_matrix[i].append(0)
            updated_matrix.append([0] * n)
        
        if new_edge:
            from_vertex, to_vertex = new_edge
            if from_vertex in updated_vertices and to_vertex in updated_vertices:
                from_idx = updated_vertices.index(from_vertex)
                to_idx = updated_vertices.index(to_vertex)
                updated_matrix[from_idx][to_idx] = 1
        
        return updated_matrix, updated_vertices

    def create_adjacency_list_from_edges(self):
        """
        Создает список смежности на основе текущих ребер графа.
        
        Returns:
            dict: словарь, где ключи - вершины, значения - списки смежных вершин
        """
        return self.adjacency_list.copy()
    
    def add_to_adjacency_list(self, adjacency_list, new_vertex=None, new_edge=None):
        """
        Добавляет вершину или ребро в существующий список смежности.
        
        Args:
            adjacency_list: текущий список смежности
            new_vertex: новая вершина для добавления (опционально)
            new_edge: кортеж (from_vertex, to_vertex) для нового ребра (опционально)
            
        Returns:
            dict: обновленный список смежности
        """
        updated_list = {key: value[:] for key, value in adjacency_list.items()}
        
        if new_vertex and new_vertex not in updated_list:
            updated_list[new_vertex] = []
        
        if new_edge:
            from_vertex, to_vertex = new_edge
            if from_vertex in updated_list and to_vertex in updated_list:
                if to_vertex not in updated_list[from_vertex]:
                    updated_list[from_vertex].append(to_vertex)
        
        return updated_list

    def __str__(self):
        return str(self.adjacency_list)
    
    

# Тестирование первого задания
if __name__ == "__main__":
    # Создаем граф
    graph = DirectedGraph()
    
    # Добавляем вершины
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_vertex('D')
    
    # Добавляем ребра
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'A')  # Обратное ребро
    
    # Выводим граф
    print("Ориентированный граф:")
    print(graph)