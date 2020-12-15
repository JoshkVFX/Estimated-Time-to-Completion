import json
from abc import abstractmethod


class Storage(object):
    @abstractmethod
    def write(self, data):
        raise RuntimeError('Write cannot be run from the base class')


class FileStorage(Storage):
    def __init__(self, path):
        self._path = path

    def write(self, data):
        with open(self._path, 'w') as f:
            f.write(data)


class Script(object):
    def __init__(self, script, storage, nodes=None):
        self._nodes = nodes or []
        self._script = script
        self._storage = storage

    @abstractmethod
    def parse(self):
        # This method needs to be overwritten by each subclass to gather the relevant definitions
        raise RuntimeError('Parse cannot be run from the base class')

    def write(self):
        self._storage.write(
            json.dumps(self._nodes)
        )


# HOW TO:
# Subclass Script for your relevant DCC
# Initialise a FileStorage object (or your own Storage subclass) with a file path
# Initialise Subclass using the Initialised Storage Object
# Feed subclass.parse into subclass.write
# Repeat for all scripts

class HoudiniScript(object):
    def __init__(self, script, storage, nodes=None):
        self._nodes = nodes or []
        self._script = script
        self._storage = storage

    @abstractmethod
    def parse(self):
        if not self._nodes:
            self._nodes = root.allSubChildren()

        all_node_data = {}
        for node in self._nodes:
            node_data = {}
            for p in node.parms():
                node_data[p.name()] = p.evalAsString()
            all_node_data[node.name()] = node_data
        return all_node_data

    def write(self):
        self._storage.write(
            json.dumps(self._nodes)
        )
