import pandas
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from datetime import datetime
import pickle

#Data
DATA = pandas.read_csv('cleaned_data.csv')
print(DATA.columns)
INVENTORY = []

def get_item_original_history(item_name):
  output = []

  filtered = DATA[DATA[item_name] != 0]
  
  for index, row in filtered.iterrows():
    output.append({
      'timestamp': row.date + ' ' + row['arrival_ timestamp'],
      'amount': row[item_name]
    })

  return output

for i in range(3, len(DATA.columns) - 1):
  item_name = DATA.columns[i]
  #Code
  history = get_item_original_history(item_name)
  history_by_date = []
  output_next_day = []
  previous_date = ""

  for item in history:
    if previous_date == item['timestamp'].split(" ")[0]:
      history_by_date[-1]['amount'] = history_by_date[-1]['amount'] + item['amount']
    else:
      history_by_date.append({
        'date': item['timestamp'].split(" ")[0],
        'amount': item['amount']
      })
      previous_date = item['timestamp'].split(" ")[0]
    
  for item in history_by_date:
    output_next_day.append(item['amount'])
  
  history_by_date.pop()
  output_next_day.pop(0)

  print(len(history_by_date), len(output_next_day))

  net = buildNetwork(2, 5, 1)
  ds = SupervisedDataSet(2, 1)
  for i in range(len(history_by_date)):
    date_timestamp = int(datetime.strptime(history_by_date[i]['date'], '%d/%m/%Y').strftime('%S'))
    ds.addSample((date_timestamp, history_by_date[i]['amount']), (output_next_day[i],))

  len(ds)

  trainer = BackpropTrainer(net, ds)
  trainer.trainUntilConvergence()

  net.activate([int(datetime.strptime('2/7/2019', '%d/%m/%Y').strftime('%S')), 16])

  # fileObj = open(item_name + '.model', 'wb')
  # pickle.dump(net, fileObj)
  # print("Done with " + item_name)
  # fileObj.close()