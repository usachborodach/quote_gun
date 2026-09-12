from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client['quote_gun']
quotes_collection = db['quotes']

@app.route('/all')
def all():
    categories = quotes_collection.distinct('category')
    categories.sort()
    return render_template('main.html', categories=categories)

@app.route('/main')
def main():
    categories = quotes_collection.distinct('category')
    categories.sort()
    exclude = ['svetlana_anatolyevna', 'shtomnepokushac']
    for i in exclude:
        categories.remove(i)
    return render_template('main.html', categories=categories)

@app.route('/chance')
def chance():
    categories = quotes_collection.distinct('category')
    categories.sort()
    exclude = ['svetlana_anatolyevna', 'vahtang']
    for i in exclude:
        categories.remove(i)
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