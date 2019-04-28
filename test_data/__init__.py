"""
Simple way to build synthetic data
"""

import random

from collections import defaultdict


def build_synthetic_data(num_of_scripts=3, num_of_nodes=3):
    estimated_times = []
    synthetic_data = []
    for script in range(num_of_scripts):
        script_time = 0
        script_data = defaultdict(list)
        for node in range(num_of_nodes):
            node_type = random.choice([SimpleANode, SimpleBNode, SimpleCNode, SimpleDNode])
            node_object = node_type()
            script_data[node_object.__class__.__name__].append(node_object)
            script_time += node_object.value
        synthetic_data.append(script_data)
        estimated_times.append(script_time)
    return synthetic_data, estimated_times


# Be sure to update the range in the 'multipliers' list generator variable inside
# the 'build_synthetic_data' function when adding more SimpleNodes classes
class SimpleNodes(object):
    __multiplier = 1
    _number_of_knobs = 10

    def __init__(self):
        self._value = 0
        self.knobs = {}

        for knob in range(self._number_of_knobs):
            value = random.randint(30, 100)
            setattr(self, 'knob%d' % knob, value)
            self.knobs['knob%d' % knob] = value
            self._value += value

    @property
    def value(self):
        return self._value * self.__multiplier


class SimpleANode(SimpleNodes):
    """
    Type A of the simple node series
    """
    __multiplier = 1
    _number_of_knobs = 14


class SimpleBNode(SimpleNodes):
    """
    Type B of the simple node series
    """
    __multiplier = 1
    _number_of_knobs = 27


class SimpleCNode(SimpleNodes):
    """
    Type C of the simple node series
    """
    __multiplier = 1
    _number_of_knobs = 5


class SimpleDNode(SimpleNodes):
    """
    Type D of the simple node series
    """
    __multiplier = 1
    _number_of_knobs = 50
