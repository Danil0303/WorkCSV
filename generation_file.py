import random
import csv

# Список брендов телефонов
brands = ['Apple', 'Samsung', 'Xiaomi']

# Название моделей телефона
models = [
    'iPhone 15 Pro',
    'Galaxy S23 Ultra',
    'Redmi Note 12',
    'Poco X5 Pro',
    'Pixel 7 Pro',
    'OnePlus 11T',
    'Honor Magic Vs',
    'Motorola Edge Plus',
    'Nokia G22',
    'Huawei Mate 50 Pro'
]

# Генерируем случайные цены от 100 до 1500 долларов
prices = range(100, 1501)

# Рейтинги от 3.0 до 5.0 с шагом 0.1
ratings = [round(x * 0.1, 1) for x in range(30, 51)]

# Создаем список товаров
data = []
for _ in range(10):  # создаем 1000 записей
    brand = random.choice(brands)
    model = random.choice(models)
    price = random.choice(prices)
    rating = random.choice(ratings)
    data.append([model, brand, price, rating])

# Записываем данные в CSV-файл
with open('phone.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'brand', 'price', 'rating'])  # заголовки столбцов
    writer.writerows(data)

print("CSV-файл успешно создан!")