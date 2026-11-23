import os
from pymongo import MongoClient
import yaml

base_path = os.path.dirname(__file__)
os.chdir(base_path)

client = MongoClient()
db = client['quote_gun']
collection = db['quotes']
cursor = collection.find({})
documents = list(cursor)

structure = {}
for document in documents:
    if document['category'] not in structure:
        structure[document['category']] = []
    structure[document['category']].append(document['text'])

os.makedirs('data', exist_ok=True)
for category, quotes in structure.items():
    with open(f'data/{category}.yml', 'w', encoding='utf-8') as file:
        yaml.safe_dump(
            quotes,
            file,
            allow_unicode=True,
            default_flow_style=False,   # блочный стиль: каждый элемент — с новой строки
            width=float('inf'),         # отключаем переносы по ширине
        )

client.close()