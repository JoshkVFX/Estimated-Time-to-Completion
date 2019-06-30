import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split


NUM_OF_SCRIPTS = 250000
NODE_TYPES = {'nodeTypeA', 'nodeTypeB', 'nodeTypeC', 'nodeTypeD', 'nodeTypeE', 'nodeTypeF'}

nodes = {'values': [], 'id': [], 'type': [], 'script_id': []}
scripts = {'execution_time': [], 'id': []}

print('BEGINNING SCRIPT AND NODE GENERATION')

nodeID = 0
for script_id in range(NUM_OF_SCRIPTS):
    # Generate nodes
    script_execution_time = 0
    for nodeType in NODE_TYPES:
        for i in range(random.randint(6, 15)):
            value = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                     random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
            nodes['values'].append(value)
            nodes['id'].append(nodeID)
            nodes['type'].append(nodeType)
            nodes['script_id'].append(script_id)
            script_execution_time += sum([x * 8 for x in value])
    scripts['execution_time'].append(script_execution_time)
    scripts['id'].append(script_id)


print('CONVERTING SCRIPTS AND NODES TO DATAFRAME')


allNodes = pd.DataFrame(nodes, columns=['values', 'id', 'type', 'script_id'])
allScripts = pd.DataFrame(scripts, columns=['execution_time', 'id'])
allNodes.set_index('id')
allScripts.set_index('id')

print('FILLING SCRIPT DATAFRAME WITH DEFAULT ZERO VALUES PER SCRIPT')

for name in NODE_TYPES:
    allScripts[name] = np.zeros(len(allScripts.values))

print('GENERATING NORMALISED INDEX VALUE FOR EACH NODE TYPE')


allNodes['normalised_index_value'] = 0
for nodeType, df in allNodes.groupby('type'):
    min_max_scaler = preprocessing.MinMaxScaler()
    sorted_values = sorted(range(len(df['values'])), key=lambda k: df['values'].values[k])
    sorted_values = np.array(sorted_values).reshape(-1, 1)
    x_scaled = min_max_scaler.fit_transform(sorted_values)

    allNodes.loc[allNodes['type'] == nodeType, 'normalised_index_value'] = x_scaled


print('BEGINNING REORGANISING OF VALUES INTO LISTS OF NODETYPES FOR EACH SCRIPT')

for (script_id, nodeType), df in allNodes.groupby(['script_id', 'type']):
    allScripts.at[script_id, nodeType] = sum(df['normalised_index_value'].values)


print('SPLIT DATA')

train_data, test_data = train_test_split(allScripts)


model = BayesianRidge()
print('TRAIN BAYESIAN MODEL BASED ON DATA')
model.fit(train_data[NODE_TYPES], train_data['execution_time'])
print('PREDICT OUTCOME OF TEST DATA USING FITTED MODEL')
prediction = model.predict(test_data[NODE_TYPES])
print('Prediction:')
print(prediction)
print('Execution time:')
print(test_data['execution_time'].values)

errors = []
for predictedValue, trueValue in zip(prediction, test_data['execution_time']):
    errors.append(int(trueValue - predictedValue))
print('Error mean:')
print(np.mean(errors))
print('Error average:')
print(np.average(errors))
print('Error standard deviation:')
std = np.std(errors)
print(std)
print('Error standard deviation percentage:')
print(std / max(test_data['execution_time']) * 100)


plt.scatter(prediction, test_data['execution_time'])
plt.show()
