from flask import Flask
from flask import jsonify
import pandas
import random

app = Flask(__name__)

DATA = pandas.read_csv('cleaned_data.csv')
INVENTORY = []

for i in range(3, len(DATA.columns) - 1):
  INVENTORY.append({
    'name': DATA.columns[i],
    'itemCode': random.randint(100000, 999999),
    'quantity': random.randint(1, 99),
    'status': 'In stock'
  })

@app.route('/')
def index_not_found():
  return jsonify({
    'error': 'Not found'
  }), 404

@app.route('/api/inventory')
def get_inventory():
  return jsonify(INVENTORY), 200