"""
Simple way to build synthetic data
"""

from kids.cache import hashing


def get_value(value):
    return value


def build_synthetic_data(num_of_scripts=3, num_of_nodes=3, num_of_knobs=10):
    import random

    synthetic_data = {}
    for script in range(num_of_scripts):
        script_time = 0
        script_data = {}
        for node in range(num_of_nodes):
            node_data = {}
            for knob in range(num_of_knobs):
                node_value = random.randint(30, 100)
                node_data['knob%s' % knob] = node_value
                script_time += get_value(node_value)
            script_data['node%s' % node] = SimpleNodes(node_data)
        synthetic_data['script%s' % script] = script_data
        synthetic_data['duration'] = script_time
    return synthetic_data


@hashing
class SimpleNodes(object):
    def __init__(self, node_dict):
        for key, value in node_dict.items():
            setattr(self, key, value)
