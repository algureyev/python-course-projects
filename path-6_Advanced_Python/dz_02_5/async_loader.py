# код из темы "Асинхронное программирование"

import pandas as pd
import io
import asyncio
import aiohttp
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import threading


class Model(ABC):
    """Абстрактный базовый класс для работы с данными с веб-сайта"""
    
    @abstractmethod
    async def get_data(self, categories):
        """Асинхронное получение информации с веб-сайта по массиву категорий"""
        pass
    
    @abstractmethod
    def parse_data(self, data):
        """Преобразование данных с сайта в словарь"""
        pass


class WoysaLoader(Model):
    """Класс для получения данных с сайта woysa.club (синглтон) с асинхронной загрузкой и многопоточностью"""
    
    _instance = None
    _url = 'https://analitika.woysa.club/images/panel/json/download/niches.php'
    _lock = threading.Lock()  # Блокировка для thread-safe операций
    

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WoysaLoader, cls).__new__(cls)
        return cls._instance
    

    async def get_data(self, categories: list[int], batch_size: int = None, max_workers: int = 5) -> pd.DataFrame:
        """
        Асинхронный метод получения данных с сайта по массиву категорий с использованием многопоточности

        Args:
            categories: список идентификаторов категорий
            batch_size: размер пакета для обработки (опционально)
            max_workers: максимальное количество потоков
            
        Returns:
            pd.DataFrame: DataFrame с объединенными данными по всем категориям
        """
       
        if not categories:
            return pd.DataFrame()
        
        # Разделение категорий на пакеты
        if batch_size:
            category_batches = self._split_categories_into_batches(categories, batch_size)
        else:
            category_batches = [categories]

        # Многопоточная обработка пакетов категорий
        all_data = await self._process_batches_with_threads(category_batches, max_workers)

        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

    async def _process_batches_with_threads(self, category_batches: List[List[int]], max_workers: int) -> List[pd.DataFrame]:
        """Многопоточная обработка пакетов категорий с использованием ThreadPoolExecutor

        Args:
            category_batches: список пакетов категорий
            max_workers: максимальное количество потоков

        Returns:
            List[pd.DataFrame]: список DataFrame с данными
        """
        
        # Создаем event loop для текущего потока
        loop = asyncio.get_event_loop()
        
        # Функция для выполнения в потоке
        def process_batch_in_thread(batch):
            # Создаем новый event loop для каждого потока
            thread_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(thread_loop)
            try:
                # Запускаем асинхронную обработку пакета
                result = thread_loop.run_until_complete(self._process_categories_batch(batch))
                return result
            finally:
                thread_loop.close()

        # Используем ThreadPoolExecutor для многопоточной обработки
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Используем map для применения функции к каждому пакету
            batch_results = list(executor.map(process_batch_in_thread, category_batches))

        # Собираем все результаты
        all_data = []
        for batch_result in batch_results:
            if batch_result:
                all_data.extend(batch_result)
        
        return all_data

    def _split_categories_into_batches(self, categories: List[int], batch_size: int) -> List[List[int]]:
        """Разделение массива категорий на пакеты с использованием np.array_split

        Args:
            categories: список категорий
            batch_size: размер пакета

        Returns:
            List[List[int]]: список пакетов категорий
        """
        arrays = np.array_split(categories, len(categories) // batch_size + 1)
        return [arr.tolist() for arr in arrays if len(arr) > 0]


    async def _process_categories_batch(self, categories: List[int]) -> List[pd.DataFrame]:
        """Асинхронная обработка пакета категорий

        Args:
            categories: список категорий для обработки

        Returns:
            List[pd.DataFrame]: список DataFrame с данными
        """

        async with aiohttp.ClientSession() as session:
            tasks = []
            for category in categories:
                task = self._fetch_category_data(session, category)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Фильтрация успешных результатов
        valid_results = []
        for category, result in zip(categories, results):
            if isinstance(result, Exception):
                print(f"Ошибка при загрузке категории {category}: {result}")
                continue
            if result is not None:
                valid_results.append(result)
        
        return valid_results
    
    async def _fetch_category_data(self, session: aiohttp.ClientSession, category: int) -> pd.DataFrame:
        """Асинхронная загрузка данных для одной категории

        Args:
            session: aiohttp сессия
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