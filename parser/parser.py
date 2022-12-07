import json

import requests


def get_category_data():
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
    for category_name, category_id in data.items():
        params = {
            "expand": "url",
            'per-page': 20,
            'category_id': category_id,
        }
        response = requests.get(url, headers=headers, params=params)
        data[category_name] = response.json()
    return data


def filter_json_data(json_file):
    thumbnail_link = 'https://img5.lalafo.com/i/posters/api'
    filtered_data = {}
    filtered_items = []
    for key, value in json_file.items():
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


def create_filtered_json_file(data):
    with open('lalafo_data.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    category_data = get_category_data()
    url = 'https://lalafo.kg/api/search/v3/feed/search'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "device": "pc"
    }
    json_data = get_json_data(category_data)
    filtered_json_data = filter_json_data(json_data)
    create_filtered_json_file(filtered_json_data)
