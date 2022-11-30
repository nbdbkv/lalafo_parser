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


category_ids = get_category_ids()

url = 'https://lalafo.kg/api/search/v3/feed/search'

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "device": "pc"
}


def get_json():
    categories = []
    for category_id in category_ids:
        params = {
            "expand": "url",
            'per-page': 16,
            'category_id': category_id,
        }
        response = requests.get(url, headers=headers, params=params)
        categories.append({
            category_id: [response.json()]
        })
    return categories


data_json = get_json()
