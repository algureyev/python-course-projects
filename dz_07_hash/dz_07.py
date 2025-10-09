class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # Инициализируем пустыми списками

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        bucket = self.table[index]
        
        # Проверяем, есть ли уже такой ключ
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Обновляем значение
                return
        
        # Если ключа нет, добавляем новую пару
        bucket.append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        
        if bucket is not None:
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    return bucket[i][1]
        return None
    
    def delete(self, key):
            index = self.hash_function(key)
            bucket = self.table[index]
            
            if bucket is not None:
                for i, (k, v) in enumerate(bucket):
                    if k == key:
                        bucket.pop(i)
                        return True
            return False
    
    def resize(self):
        """
        Увеличивает размер хеш-таблицы вдвое и перераспределяет все элементы.
        """
        old_table = self.table
        old_size = self.size
        
        self.size *= 2
        self.table = [None] * self.size
        
        for i in range(old_size):
            if old_table[i] is not None:
                for key, value in old_table[i]:
                    index = self.hash_function(key)
                    if self.table[index] is None:
                        self.table[index] = []
                    self.table[index].append((key, value))

    def string_hash(self, s):
        """
        Функция, которая принимает строку и возвращает её хеш-значение.
        """
        hash_value = 0
        for char in s:
            hash_value += ord(char)
        return hash_value

# Тестирование работы метода resize

# Создаем таблицу с начальным размером 5
ht = HashTable(5)
print(f"Начальный размер: {ht.size}")

# Добавляем 10 элемента
for i in range(10):
    ht.insert(f"key{i}", f"value{i}")

print(f"Размер после добавления 10 элементов: {ht.size}")

ht.resize()
print(f"Размер после вызова resize: {ht.size}")

# Проверяем, что все элементы на месте
for i in range(10):
    print(f"key{i}: {ht.search(f'key{i}')}")

# Просто используем встроенный словарь
print("___________________________")

my_dict = {}

# Добавление элементов с хеш-значениями
my_dict["apple"] = (ht.string_hash("apple"), "fruit")
my_dict["carrot"] = (ht.string_hash("carrot"), "vegetable")

# Поиск
key = "apple"
if key in my_dict:
    hash_val, value = my_dict[key]
    print(f"Ключ: {key}, Хеш: {hash_val}, Значение: {value}")