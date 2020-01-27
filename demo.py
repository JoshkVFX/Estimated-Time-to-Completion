import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sys
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
from interpolator import generate_relative_normalised_values, generate_normalised_values
from evaluate import EvaluationModel


def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nodes', nargs='?', type=int, dest='num_nodes',
                        help='Number of synthetic nodes each script should have.\n'
                             'If not passed a random value between 50 and 100 will be chosen')
    parser.add_argument('-s', '--scripts', nargs='?', default=10000, type=int, dest='num_scripts',
                        help='Number of synthetic scripts to generate for the synthetic dataset.\n'
                             'Default: 10000')
    parser.add_argument('-t', '--types', nargs='*', action='append', dest='node_types',
                        default=['nodeTypeA', 'nodeTypeB', 'nodeTypeC', 'nodeTypeD', 'nodeTypeE', 'nodeTypeF'],
                        help='Number of synthetic node types to pass into the synthetic data generator')
    return parser.parse_args()


def build_synthetic_data(num_of_scripts, num_of_nodes, node_types):
    nodes = {'values': [], 'id': [], 'type': [], 'script_id': []}
    scripts = {'execution_time': [], 'id': []}
    nodeID = 0
    for script_id in range(num_of_scripts):
        # Generate nodes
        script_execution_time = 0
        for node_type in node_types:
            for i in range(num_of_nodes or random.randint(10, 100)):
                value = (random.random(), random.random(), random.random(),
                         random.random(), random.random(), random.random())
                nodes['values'].append(value)
                nodes['id'].append(nodeID)
                nodes['type'].append(node_type)
                nodes['script_id'].append(script_id)
                script_execution_time += sum(value)
        scripts['execution_time'].append(script_execution_time)
        scripts['id'].append(script_id)
    return nodes, scripts


def main(num_of_scripts, num_of_nodes, node_types):
    print('BEGINNING SCRIPT AND NODE GENERATION')
    nodes, scripts = build_synthetic_data(num_of_scripts, num_of_nodes, node_types)

    print('CONVERTING SCRIPTS AND NODES TO DATAFRAME')

    allNodes = pd.DataFrame(nodes, columns=nodes.keys())
    allScripts = pd.DataFrame(scripts, columns=scripts.keys())
    allNodes.set_index('id')
    allScripts.set_index('id')

    print('FILLING SCRIPT DATAFRAME WITH DEFAULT ZERO VALUES PER SCRIPT')

    for name in node_types:
        allScripts[name] = np.zeros(len(allScripts.values))

    print('GENERATING NORMALISED INDEX VALUE FOR EACH NODE TYPE')

    allNodes = generate_normalised_values(allNodes)

    print('BEGINNING REORGANISING OF VALUES INTO LISTS OF NODETYPES FOR EACH SCRIPT')

    allScripts = generate_relative_normalised_values(allNodes, allScripts)

    print('SPLIT DATA')

    train_data, test_data = train_test_split(allScripts)

    model = EvaluationModel(model=BayesianRidge)
    print('TRAIN MODEL BASED ON DATA')
    model.fit(train_data[node_types], train_data['execution_time'])
    print('PREDICT OUTCOME OF TEST DATA USING FITTED MODEL')
    prediction = model.predict(test_data[node_types])
    print('Prediction:')
    print(prediction)
    print('Execution time:')
    print(test_data['execution_time'].values)

    errors, mean, average, minimum, maximum, std, std_percentage = model.evaluate_error_from_last_prediction(
        test_data['execution_time'])
    print('Error mean:')
    print(mean)
    print('Error average:')
    print(average)
    print('Min/Max error:')
    print('%s/%s' % (minimum, maximum))
    print('Error standard deviation:')
    print(std)
    print('Error standard deviation percentage:')
    print(std_percentage)

    plt.scatter(prediction, test_data['execution_time'])
    plt.show()

    plt.hist(errors, color='red')
    plt.show()


if __name__ == '__main__':
    args = argumentParser()
    sys.exit(main(args.num_scripts, args.num_nodes, args.node_types))
