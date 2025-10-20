import requests
import pandas as pd
from abc import ABC, abstractmethod


class Model(ABC):
    """Абстрактный базовый класс для работы с данными с веб-сайта"""
    
    @abstractmethod
    def get_data(self, categories):
        """Получение информации с веб-сайта по массиву категорий"""
        pass
    
    @abstractmethod
    def parse_data(self, data):
        """Преобразование данных с сайта в словарь"""
        pass


class WoysaLoader(Model):
    """Класс для получения данных с сайта woysa.club (синглтон)"""
    
    _instance = None
    _url = 'https://analitika.woysa.club/images/panel/json/download/niches.php'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WoysaLoader, cls).__new__(cls)
        return cls._instance
    
    def get_data(self, categories):
        """Получение данных с сайта по массиву категорий"""
        if not categories:
            return pd.DataFrame()
        
        all_data = []
        for category in categories:
            params = {
                'skip': 0,
                'price_min': 0,
                'price_max': 1060225,
                'up_vy_min': 0,
                'up_vy_max': 108682515,
                'up_vy_pr_min': 0,
                'up_vy_pr_max': 2900,
                'sum_min': 1000,
                'sum_max': 82432725,
                'feedbacks_min': 0,
                'feedbacks_max': 32767,
                'trend': 'false',
                'sort': 'sum_sale',
                'sort_dir': -1,
                'id_cat': category
            }
            
            response = requests.get(self._url, params=params)
            if response.status_code == 200:
                df = pd.read_excel(response.content)
                df['category'] = category
                all_data.append(df)
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    
    def parse_data(self, data):
        """Преобразование DataFrame в словарь"""
        return data.to_dict('records') if not data.empty else {}


# Пример использования
if __name__ == "__main__":
    loader = WoysaLoader()
    
    # Получаем данные по категориям
    categories = [10000, 15000]
    data_frame = loader.get_data(categories)

    print("Первые 5 строк полученого датафрейма")
    print(data_frame.head())

    # Преобразуем в словарь
    data_dict = loader.parse_data(data_frame)

    print("Первые 2 записи из словаря")
    for i, record in enumerate(data_dict[:2]):
        print(f"Запись {i+1}: {record}")
    
    print(f"Получено {len(data_frame)} записей")
    print(f"Преобразовано в {len(data_dict)} словарей")