from flask import Flask
from flask import jsonify

import pandas
import random

app = Flask(__name__)

DATA = pandas.read_csv('cleaned_data.csv')
print(DATA.columns)
INVENTORY = []

for i in range(3, len(DATA.columns) - 1):
  INVENTORY.append({
    'name': DATA.columns[i],
    'itemCode': random.randint(100000, 999999),
    'quantity': random.randint(1, 99),
    'status': 'In stock'
  })

def get_item_name(code):
  for i in range(len(INVENTORY)):
    if code == INVENTORY[i]['itemCode']:
      return INVENTORY[i]['name']

def get_item_original_history(item_name):
  output = []

  filtered = DATA[DATA[item_name] != 0]
  
  for index, row in filtered.iterrows():
    output.append({
      'timestamp': row.date + ' ' + row['arrival_ timestamp'],
      'amount': row[item_name]
    })
  
  return output

@app.route('/')
def index_not_found():
  return jsonify({
    'error': 'Not found'
  }), 404

@app.route('/api/inventory')
def get_inventory():
  return jsonify(INVENTORY), 200

@app.route('/api/history/<int:item_code>')
def get_item_history(item_code):
  item_name = get_item_name(item_code)

  original = get_item_original_history(item_name)

  return jsonify({
    'original': original,
    'statistics': [],
    'machine': []
  }), 200