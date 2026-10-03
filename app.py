from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient

HIDDEN_CATEGORIES = ['svetlana_anatolyevna', 'fake_chinese', 'jokes']

app = Flask(__name__)
client = MongoClient()
db = client['quote_gun']
quotes_collection = db['quotes']

@app.route('/')
def all():
    categories = quotes_collection.distinct('category')
    categories.sort()
    for i in HIDDEN_CATEGORIES:
        categories.remove(i)
        categories.sort()
    return render_template('main.html', categories=categories)

@app.route('/<category>')
def quotes_by_category(category):
    pipeline = [
        {"$match": {"category": category}},
        {"$sample": {"size": 10}}
    ]
    docs = list(quotes_collection.aggregate(pipeline))
    items = [doc['text'] for doc in docs]
    return render_template('quotes.html', items=items, category=category)

@app.route('/favicon.png')
def favicon():
    return send_from_directory('static', 'favicon.png')