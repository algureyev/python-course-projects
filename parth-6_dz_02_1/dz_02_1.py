import requests
import pandas as pd
import io
import subprocess
import tempfile
import os

class Model:
    url = 'https://analitika.woysa.club/images/panel/json/download/niches.php'

    def download(self, skip, category):  
        url = self.url + f"?skip={skip}&price_min=0&price_max=1060225&up_vy_min=0&up_vy_max=108682515&up_vy_pr_min=0&up_vy_pr_max=2900&sum_min=1000&sum_max=82432725&feedbacks_min=0&feedbacks_max=32767&trend=false&sort=sum_sale&sort_dir=-1&id_cat={category}"
        return requests.get(url)

# Тестовый вызов
model = Model()
response = model.download(100, 10000)

print("Статус код:", response.status_code)
print("Тип содержимого:", response.headers.get('Content-Type'))

if response.status_code == 200:
    # Сохраняем временный файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
        tmp_file.write(response.content)
        temp_path = tmp_file.name
    
    try:
        # Пробуем разные движки
        engines = [None, 'openpyxl', 'xlrd', 'calamine']
        
        for engine in engines:
            try:
                df = pd.read_excel(temp_path, engine=engine)
                print(f"✅ Успех с движком: {engine}")
                break
            except:
                continue
        else:
            print("❌ Ни один движок не сработал")
            
        # Выводим результат
        print(f"\n📊 ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ:")
        print(f"Размер: {df.shape[0]} строк × {df.shape[1]} столбцов")
        print(f"\nПервые 10 строк:")
        print(df.head(10))
        print(f"\nСтолбцы: {list(df.columns)}")
        
    finally:
        # Удаляем временный файл
        os.unlink(temp_path)