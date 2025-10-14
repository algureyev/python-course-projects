class BinaryTree:
    """Класс BinaryTree реализует бинарное дерево"""
    
    def __init__(self):
        """Инициализация пустого дерева"""
        self.value = None
        self.left = None
        self.right = None
    
    def insert(self, value):
        """
        Вставка элемента в бинарное дерево
        
        Args:
            value: значение для вставки
        """
        if self.value is None:
            self.value = value
            self.left = BinaryTree()
            self.right = BinaryTree()
        else:
            if value < self.value:
                self.left.insert(value)
            else:
                self.right.insert(value)
    
    def search(self, value):
        """
        Поиск элемента в бинарном дереве
        
        Args:
            value: значение для поиска
            
        Returns:
            bool: True если найден, False если нет
        """
        if self.value is None:
            return False
        
        if value == self.value:
            return True
        elif value < self.value:
            return self.left.search(value)
        else:
            return self.right.search(value)
        
    def bfs(self):
        """
        Обход бинарного дерева в ширину (Breadth-First Search)
        
        Returns:
            list: список значений в порядке обхода BFS
        """
        if self.value is None:
            return []
        
        result = []
        queue = [self]  # Используем список как очередь
        
        while queue:
            current = queue.pop(0)  
            
            if current.value is not None:
                result.append(current.value)
                
                if current.left.value is not None:
                    queue.append(current.left)
                if current.right.value is not None:
                    queue.append(current.right)
        
        return result

    def dfs_preorder(self):
        """
        Прямой обход в глубину (Preorder DFS)
        Порядок: корень → левое поддерево → правое поддерево
        """
        if self.value is None:
            return []
        
        result = [self.value]
        result.extend(self.left.dfs_preorder())
        result.extend(self.right.dfs_preorder())
        return result
    
    def dfs_inorder(self):
        """
        Симметричный обход в глубину (Inorder DFS)
        Порядок: левое поддерево → корень → правое поддерево
        """
        if self.value is None:
            return []
        
        result = []
        result.extend(self.left.dfs_inorder())
        result.append(self.value)
        result.extend(self.right.dfs_inorder())
        return result
    
    def dfs_postorder(self):
        """
        Обратный обход в глубину (Postorder DFS)
        Порядок: левое поддерево → правое поддерево → корень
        """
        if self.value is None:
            return []
        
        result = []
        result.extend(self.left.dfs_postorder())
        result.extend(self.right.dfs_postorder())
        result.append(self.value)
        return result

class AVLTree(BinaryTree):
    """Класс AVLTree наследует BinaryTree и добавляет балансировку"""
    
    def __init__(self):
        """Инициализация AVL дерева"""
        super().__init__()
    
    def left_rotate(self):
        """
        Левый поворот
        """
        if self.right.value is None:
            return self
            
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        
        return new_root
    
    def right_rotate(self):
        """
        Правый поворот
        """
        if self.left.value is None:
            return self
            
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        
        return new_root
    
    def rebalance(self):
        """
        Балансировка дерева
        Простая реализация - всегда делает правый поворот для демонстрации
        """
        print("Выполняем балансировку...")
        return self.right_rotate()