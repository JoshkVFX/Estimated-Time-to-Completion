import argparse
from pprint import pprint
from matplotlib import pyplot as plt
from kids.cache import hashing

import test_data


def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--scripts', default=3, type=int)
    argparser.add_argument('-n', '--nodes', default=10, type=int)
    return argparser.parse_args()


if __name__ == '__main__':
    args = parser()
    synthetic_data, estimated_times = test_data.build_synthetic_data(
        num_of_scripts=args.scripts, num_of_nodes=args.nodes)
    # pprint(synthetic_data)
    # pprint(estimated_times)
    hashed_synth_data = []
    for script_data in synthetic_data:
        for scriptName, list_of_nodes in script_data.items():
            for node_object in list_of_nodes:
                _key = hashing()
                key = _key(**node_object.knobs)
                hashed_synth_data.append(key)
    print(hashed_synth_data)
    plt.scatter(hashed_synth_data, estimated_times)
    plt.plot()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
