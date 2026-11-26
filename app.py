import os
import random

import yaml
from flask import Flask, abort, jsonify, render_template, send_from_directory

HIDDEN_CATEGORIES = ['svetlana_anatolyevna', 'jokes']
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

app = Flask(__name__)


def category_exists(category):
    return (
        os.path.basename(category) == category
        and os.path.isfile(os.path.join(DATA_DIR, category + '.yml'))
    )


@app.route('/')
def all():
    categories = sorted(
        os.path.splitext(f)[0] for f in os.listdir(DATA_DIR) if f.endswith('.yml')
    )
    for i in HIDDEN_CATEGORIES:
        if i in categories:
            categories.remove(i)
    return render_template('main.html', categories=categories)


@app.route('/<category>')
def quotes_by_category(category):
    if not category_exists(category):
        abort(404)
    quotes = load_category(category) or []
    items = random.sample(quotes, min(10, len(quotes)))
    return render_template('quotes.html', items=items, category=category)


def load_category(category):
    path = os.path.join(DATA_DIR, category + '.yml')
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


@app.route('/api/quotes')
def api_all_quotes():
    categories = sorted(
        os.path.splitext(f)[0] for f in os.listdir(DATA_DIR) if f.endswith('.yml')
    )
    result = []
    for category in categories:
        quotes = load_category(category) or []
        result.append({
            'category': category,
            'hidden': category in HIDDEN_CATEGORIES,
            'count': len(quotes),
            'quotes': quotes,
        })
    return jsonify({'total': sum(c['count'] for c in result), 'categories': result})


@app.route('/api/quotes/<category>')
def api_quotes_by_category(category):
    if not category_exists(category):
        abort(404)
    quotes = load_category(category) or []
    return jsonify({
        'category': category,
        'hidden': category in HIDDEN_CATEGORIES,
        'count': len(quotes),
        'quotes': quotes,
    })


@app.route('/favicon.png')
def favicon():
    return send_from_directory('static', 'favicon.png')
