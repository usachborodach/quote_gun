import os
from pymongo import MongoClient
import yaml

base_path = os.path.dirname(__file__)
os.chdir(base_path)

client = MongoClient()
db = client['quote_gun']
collection = db['quotes']
cursor = collection({})
documents = list(cursor)

structure = dict()
for document in documents:
    if document['category'] not in structure.keys():
        structure[document['category']] = list
    structure[document['category']].append(document['text'])

for category, quotes in structure.items():
    with open(f'data/{category}.yml', 'w') as file:
        yaml.safe_dump(quotes, allow_unicode=True)

client.close()