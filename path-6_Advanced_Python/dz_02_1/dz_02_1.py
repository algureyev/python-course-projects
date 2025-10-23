import requests
import pandas as pd
import io
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
    
    def get_data(self, categories: list[int]) -> pd.DataFrame:
        """
        Получение данных с сайта по массиву категорий

        Args:
            categories: список идентификаторов категорий
            
        Returns:
            pd.DataFrame: DataFrame с объединенными данными по всем категориям
        """
        if not categories:
            return pd.DataFrame()
        
        all_data = []
        session = requests.Session()

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
            
            try:
                response = session.get(self._url, params=params, timeout=10)
                response.raise_for_status()
            
                df = pd.read_excel(io.BytesIO(response.content))
                df['category'] = category
                all_data.append(df)
            
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе категории {category}: {e}")
                continue
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    
    def parse_data(self, data: pd.DataFrame) -> list[dict]:
        """
        Преобразование DataFrame в словарь
        
        Args:
            data: DataFrame для преобразования
            
        Returns:
            list[dict]: список словарей с данными
            
        """
        return data.to_dict('records') if not data.empty else {}


# Пример использования
if __name__ == "__main__":
    loader = WoysaLoader()
    
    # Получаем данные по категориям
    categories = [10000, 15000]
    data_frame = loader.get_data(categories)

    print("Первые 2 строки полученого датафрейма")
    print(data_frame.head(2))

    # Преобразуем в словарь
    data_dict = loader.parse_data(data_frame)

    print("Первые 2 записи из словаря")
    for i, record in enumerate(data_dict[:2]):
        print(f"Запись {i+1}: {record}")
    
    print(f"Получено {len(data_frame)} записей")
    print(f"Преобразовано в {len(data_dict)} словарей")

