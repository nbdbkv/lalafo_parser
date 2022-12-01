import json

import requests


def get_category_ids():
    ids = []
    with open('links') as links_file:
        lines = links_file.readlines()
        for link_id in lines:
            if link_id.__contains__("category_id"):
                start = link_id.find("category_id=") + len("category_id=")
                end = link_id.find(" ")
                ids.append(link_id[start:end])
    return ids


def get_json():
    categories = {}
    for category_id in category_ids:
        params = {
            "expand": "url",
            'per-page': 20,
            'category_id': category_id,
        }
        response = requests.get(url, headers=headers, params=params)
        categories[category_id] = response.json()
    return categories


def get_data_from_json(json_file):
    thumbnail_link = 'https://img5.lalafo.com/i/posters/api'
    filtered_data = {}
    filtered_items = []
    for category_id, value in json_file.items():
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
        filtered_data[category_id] = filtered_items
        filtered_items = []
    return filtered_data


def create_filtered_json(data):
    with open('lalafo_data.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    category_ids = get_category_ids()
    url = 'https://lalafo.kg/api/search/v3/feed/search'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "device": "pc"
    }
    data_json = get_json()
    filtered_json = get_data_from_json(data_json)
    create_filtered_json(filtered_json)
