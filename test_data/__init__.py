"""
Simple way to build synthetic data
"""

import random
import pandas as pd


def build_synthetic_data(num_of_scripts=3, num_of_nodes=3):
    all_estimated_times = []
    all_nodes = []
    for script in range(num_of_scripts):
        nodes = []
        for node in range(num_of_nodes):
            # TODO: Add variation to the evaulation time based on a random multiplier
            # to simulate different types of nodes
            nodes.append(generate_knobs_and_value())
        all_estimated_times.append(evaluation_time(nodes))
        all_nodes.append(nodes)
    data = {
        'totalTime': all_estimated_times,
        'nodes': all_nodes,
    }
    return pd.DataFrame(data)


def evaluation_time(nodes):
    return sum(sum(x) for x in nodes)


def generate_multiplier(multiplier=None):
    return multiplier or random.choices([1, 15, 7, 12, 3])


def generate_knobs_and_value(number_of_knobs=None):
    number_of_knobs = number_of_knobs or random.choice([10, 14, 27, 5, 50])
    values = []
    for knob in range(number_of_knobs):
        values.append(random.randint(30, 100))
    return values
