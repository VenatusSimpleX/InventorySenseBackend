from flask import Flask
from flask import jsonify
from flask_cors import CORS
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from datetime import datetime

import pandas
import pickle
import random

app = Flask(__name__)
CORS(app)

DATA = pandas.read_csv('cleaned_data.csv')
print(DATA.columns)
INVENTORY = []

for i in range(3, len(DATA.columns) - 1):
  INVENTORY.append({
    'name': DATA.columns[i],
    'itemCode': random.randint(100000, 999999),
    'quantity': random.randint(1, 99),
    'status': 'In stock',
    'prediction': {
      'statistic': 0,
      'machine': 0
    }
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
      'timestamp': datetime.strptime(row.date, '%d/%m/%Y').strftime('%m/%d/%Y') + ' ' + row['arrival_ timestamp'],
      'amount': row[item_name]
    })
  
  return output

def get_item_statistic_history(item_name):
  return []

def get_item_machine_history(item_name):
  output = []

  filtered = DATA[DATA[item_name] != 0]

  fileObj = open(item_name + '.model', 'rb')
  net = pickle.load(fileObj)
#  int(datetime.strptime('2/7/2019', '%d/%m/%Y').strftime('%S'))
  
  for index, row in filtered.iterrows():
    output.append({
      'timestamp': datetime.strptime(row.date, '%d/%m/%Y').strftime('%m/%d/%Y') + ' ' + row['arrival_ timestamp'],
      'amount': net.activate([int(datetime.strptime(row.date, '%d/%m/%Y').strftime('%S')), row[item_name]])[0]
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
  statistics = get_item_statistic_history(item_name)
  machine = get_item_machine_history(item_name)

  return jsonify({
    'original': original,
    'statistics': statistics,
    'machine': machine
  }), 200