import asyncio
import json
import time

import httpx
import requests


def get_category_data():
    """Получает название и ID категории с файла ссылок."""
    categories = {}
    with open('links') as links_file:
        lines = links_file.readlines()
        for line in lines:
            if line.__contains__("category_id") and line.__contains__("a."):
                start_id = line.find("category_id=") + len("category_id=")
                end_id = line.find(" ")
                start_name = line.find("a. ") + len("a. ")
                end_name = line.find(" .a")
                categories[line[start_name:end_name]] = line[start_id:end_id]
    return categories


def get_json_data(data):
    """
    Парсит данные с lalafo согласно ID категории
    и записывает по ключу названию как словарь.
    """
    start_time = time.time()
    for category_name, category_id in data.items():
        params = {
            "expand": "url",
            'per-page': 1000,
            'category_id': category_id,
        }
        response = requests.get(url, headers=headers, params=params)
        data[category_name] = response.json()
    print(f"--- {time.time() - start_time} seconds ---")
    return data


async def get_category(category_id):
    """Асинхронно парсит данные с lalafo согласно ID категории."""
    async with httpx.AsyncClient() as client:
        url = f'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=1000&category_id={category_id}'
        response = await client.get(url, headers=headers)
        return response.json()


async def get_async_json_data(data):
    """Создает данные по ключу названию категории как словарь."""
    start_time = time.time()
    tasks = []
    for category_name, category_id in data.items():
        tasks.append(asyncio.create_task(get_category(category_id)))
    results = await asyncio.gather(*tasks)
    print(f"--- {time.time() - start_time} seconds ---")
    return dict(zip(data.keys(), results))


def filter_json_data(json_data):
    """Фильтрует необходимые поля объявлений с lalafo."""
    thumbnail_link = 'https://img5.lalafo.com/i/posters/api'
    filtered_data = {}
    filtered_items = []
    for key, value in json_data.items():
        for index, item in enumerate(value['items']):
            if index == 20:
                break
            title = item['title']
            description = item['description'].replace('\n', ' ')
            price = item['price']
            city = item['city']
            try:
                thumbnail = thumbnail_link + item['image']
            except TypeError:
                thumbnail = 'Без изображения'
            images = []
            for i in item['images']:
                image = i['original_url']
                images.append(image)
            phone = item['mobile']
            try:
                author = item['user']['username']
            except:
                author = ''
            filtered_items.append({
                'title': title,
                'description': description,
                'price': price,
                'city': city,
                'thumbnail': thumbnail,
                'images': images,
                'phone': phone,
                'author': author,
            })
        filtered_data[key] = filtered_items
        filtered_items = []
    return filtered_data


def create_filtered_json_file(filtered_data):
    """Создает новый фильтрованный файл."""
    with open('lalafo_data.json', 'w', encoding='UTF-8') as file:
        json.dump(filtered_data, file, indent=2, ensure_ascii=False)


def get_category_from_db():
    """Получает существующие категории с PostgreSQL."""
    response = requests.get("http://localhost:8000/api/categories/")
    return response.json()


def post_category_to_db(new_category):
    """Записывает новую категорию в PostgreSQL."""
    payload = {'name': new_category}
    response = requests.post("http://localhost:8000/api/categories/", json=payload)
    return response


def check_category_in_db(filtered_data):
    """
    Проверяет категорию на наличие в PostgreSQL.
    При отсутствии записывает.
    """
    category_from_db = get_category_from_db()
    categories = {}
    for category in [*filtered_data]:
        if not category_from_db:
            post_category_to_db(category)
        for pair in category_from_db:
            if category in pair['name']:
                categories[category] = pair['id']
            else:
                post_category_to_db(category)
    return categories


def post_json_to_postgres(filtered_data):
    """Записывает фильтрованные объявления в PostgreSQL"""
    for _ in range(1):
        check_category_in_db(filtered_data)
    categories = check_category_in_db(filtered_data)
    for key_1, value_1 in filtered_data.items():
        for name, id in categories.items():
            if key_1 == name:
                for item in value_1:
                    images = [dict(zip(['image_link'], [x])) for x in item['images']]
                    payload = {
                        'title': item['title'],
                        'description': item['description'],
                        'price': item['price'],
                        'city': item['city'],
                        'category': id,
                        'thumbnail_link': item['thumbnail'],
                        'images': images,
                        'phone': item['phone'],
                        'author': item['author']
                    }
                    response = requests.post("http://localhost:8000/api/categories/" + str(id) + "/", json=payload)
    return response


if __name__ == '__main__':
    category_data = get_category_data()
    url = 'https://lalafo.kg/api/search/v3/feed/search'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "device": "pc"
    }
    # json_data = get_json_data(category_data)
    json_data = asyncio.run(get_async_json_data(category_data))
    filtered_json_data = filter_json_data(json_data)
    create_filtered_json_file(filtered_json_data)
    post_json_to_postgres(filtered_json_data)
