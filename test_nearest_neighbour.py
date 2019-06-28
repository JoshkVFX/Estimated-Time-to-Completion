import pandas as pd
import random
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split

nodes = {'values': [], 'id': [], 'type': []}
scripts = {'execution_time': [], 'node_ids': []}

nodeID = 0
for script in range(100):
    # Generate nodes
    script_execution_time = 0
    nodeIDs = []
    for i in range(35):
        nodeType = random.choice(['nodeTypeA', 'nodeTypeB', 'nodeTypeC', 'nodeTypeD', 'nodeTypeE', 'nodeTypeF'])
        value = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                 random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        nodes['values'].append(value)
        nodes['id'].append(nodeID)
        nodes['type'].append(nodeType)
        script_execution_time += sum([x * 36 for x in value ])
        nodeIDs.append(nodeID)
        nodeID += 1
    scripts['execution_time'].append(script_execution_time)
    scripts['node_ids'].append(nodeIDs)


allNodes = pd.DataFrame(nodes, columns=['values', 'id', 'type'])
allScripts = pd.DataFrame(scripts, columns=['execution_time', 'node_ids'])


allNodes['normalised_index_value'] = 0
for nodeType, df in allNodes.groupby('type'):
    min_max_scaler = preprocessing.MinMaxScaler()
    sorted_values = sorted(range(len(df['values'])), key=lambda k: df['values'].values[k])
    sorted_values = np.array(sorted_values).reshape(-1, 1)
    x_scaled = min_max_scaler.fit_transform(sorted_values)

    allNodes.loc[allNodes['type'] == nodeType, 'normalised_index_value'] = x_scaled

node_type_value_per_scripts = []
execution_times = []
for execution_time, node_ids in allScripts.values:
    node_type_value_per_script = []
    for nodeType, values in allNodes.loc[allNodes['id'].isin(node_ids), ['normalised_index_value', 'type']].groupby('type'):
        node_type_value_per_script.append(sum(values['normalised_index_value']))
    execution_times.append(execution_time)
    node_type_value_per_scripts.append(node_type_value_per_script)


test = pd.DataFrame({'script_node_weights': node_type_value_per_scripts, 'execution_times': execution_times})


weights_train_data = test['script_node_weights'][0:80]
weights_test_data = test['script_node_weights'][81:100]
execution_train_data = test['execution_times'][0:80]
execution_test_data = test['execution_times'][81:100]
model = BayesianRidge()
model.fit(weights_train_data, execution_train_data)
prediction = model.predict(weights_test_data)
print('Prediction:')
print(prediction)
print('Execution time:')
print(execution_test_data)
