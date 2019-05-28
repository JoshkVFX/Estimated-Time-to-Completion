import argparse
from matplotlib import pyplot as plt

import test_data


def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--scripts', default=3, type=int)
    argparser.add_argument('-n', '--nodes', default=10, type=int)
    return argparser.parse_args()


if __name__ == '__main__':
    args = parser()
    dataFrame = test_data.build_synthetic_data(num_of_scripts=args.scripts, num_of_nodes=args.nodes)

    dataFrame.plot.scatter(x='totalTime', y='nodes')
    plt.show()
