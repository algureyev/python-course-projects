import pandas as pd
import io
import asyncio
import aiohttp
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Model(ABC):
    """Абстрактный базовый класс для работы с данными с веб-сайта"""
    
    @abstractmethod
    async def get_data(self, categories):
        """Асинронное получение информации с веб-сайта по массиву категорий"""
        pass
    
    @abstractmethod
    def parse_data(self, data):
        """Преобразование данных с сайта в словарь"""
        pass


class WoysaLoader(Model):
    """Класс для получения данных с сайта woysa.club (синглтон) с асинхронной загрузкой"""
    
    _instance = None
    _url = 'https://analitika.woysa.club/images/panel/json/download/niches.php'
    

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WoysaLoader, cls).__new__(cls)
        return cls._instance
    

    async def get_data(self, categories: list[int], batch_size: int = None) -> pd.DataFrame:
        """
        Асинхронный метод получения данных с сайта по массиву категорий

        Args:
            categories: список идентификаторов категорий
            batch_size: размер пакета для обработки (опционально)
            
        Returns:
            pd.DataFrame: DataFrame с объединенными данными по всем категориям
        """
       
       # Разделение категорий на пакеты
        if not categories:
            return pd.DataFrame()
        
        if batch_size:
            category_batches = self._split_categories_inti_batches(categories, batch_size)
        else:
            category_batches = [categories]

        all_data = []

        # Обработка каждого пакета с категориями

        for batch in category_batches:
            batch_data = await self._process_categories_batch(batch)
            all_data.extend(batch_data)

        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


    def _split_categories_inti_batches(self, categories: List[int], batch_size: int) -> List[List[int]]:
        """Разделение массива категорий на пакеты

        Args:
            categories: список категорий
            batch_size: размер пакета

        Returns:
            List[List[int]]: список пакетов категорий
        """
        arrays = np.array_split(categories, len(categories) // batch_size + 1)
        return [arr.tolist() for arr in arrays if len(arr) > 0]


    async def _process_categories_batch(self, categories: List[int]) -> List[pd.DataFrame]:
        """Обработка пакета категорий с использованием асинхронных запросов

        Args:
            categories: список категорий для обработки

        Returns:
            List[pd.DataFrame]: список DateFrame с данными
        """

        async with aiohttp.ClientSession() as session:
            tasks = []
            for category in categories:
                task = self._fetch_category_data(session, category)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Фильтрация успешных результатов + визуализация какие категории не загрузились
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Ошибка при загрузке категории: {result}")
                continue
            if result is not None:
                valid_results.append(result)
        
        return valid_results
    
    async def _fetch_category_data(self, session: aiohttp.ClientSession, category: int) -> pd.DataFrame:
        """Асинхронная загрузка данных для одной категории

        Args:
            session: aiohttp ceссия
            category: идентификатор категории

        Returns:
            pd.DataFrame: DataFrame с данными категории
        """
        
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
            async with session.get(self._url, params=params, timeout=10) as response:
                response.raise_for_status()
                
                content = await response.read()
                df = pd.read_excel(io.BytesIO(content))
                df['category'] = category
                return df
                
        except Exception as e:
            print(f"Ошибка при запросе категории {category}: {e}")
            return None
    
    def parse_data(self, data: pd.DataFrame) -> list[dict]:
        """
        Преобразование DataFrame в словарь
        
        Args:
            data: DataFrame для преобразования
            
        Returns:
            list[dict]: список словарей с данными
            
        """
        return data.to_dict('records') if not data.empty else []


# Пример использования
async def main():
    loader = WoysaLoader()

     
    # Получаем данные по категориям, которые разбиты на пакеты
    categories = [10000, 15000, 20000, 21000]
    data_frame = await loader.get_data(categories, batch_size=2)

    print("Первые 2 строки полученого датафрейма")
    print(data_frame.head(2))

    # Преобразуем в словарь
    data_dict = loader.parse_data(data_frame)

    print("Первые 2 записи из словаря")
    for i, record in enumerate(data_dict[:2]):
        print(f"Запись {i+1}: {record}")
    
    print(f"Получено {len(data_frame)} записей")
    print(f"Преобразовано в {len(data_dict)} словарей")

if __name__ == "__main__":
    asyncio.run(main())