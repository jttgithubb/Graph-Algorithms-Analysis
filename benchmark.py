# Module for benchmarking different bin-packing algorithms on different input sizes n and waste W(A)
# 1. Enter the algorithm name and number of items
# 2. Run benchmark and calculate the waste (goal of 50 datapoints per size n)
# 3. Record in a separate csv file for each algorithm

from graph_algorithms import get_diameter, get_clustering_coefficient, get_degree_distribution
from graph import Graph
import argparse
import random
from pathlib import Path
from math import log, log2

# Path object or folder for storing our collected data
DATA_DIRECTORY = Path('data')

GRAPH_ALGORITHMS = {
    'get_diameter': get_diameter,
    'get_clustering_coefficient': get_clustering_coefficient,
    'get_degree_distribution': get_degree_distribution
}

parser = argparse.ArgumentParser(
    prog= 'Benchmark',
    description= 'Benchmarking different graph algorithms on different input sizes n',
    epilog= 'Happy Graphing!'
)

parser.add_argument('algorithm', choices=GRAPH_ALGORITHMS.keys(), help='Graph algorithm')
parser.add_argument('size', type=int, help='Size of input list')

def generate_er_graph(size: int):
    p = 2 * log(size) / size
    print(p)
    edges = []
    for i in range(size):
        for j in range(i+1, size):
            if random.random() < p:
                edges.append((i, j))
    return Graph(size, edges)

def fast_generate_er_graph(size: int):
    p = 2 * log(size) / size
    edges = set()
    v = 1
    w = -1
    while v < size:
        r = random.random()
        w = w + 1 + (int(log2(1-r) / log2(1-p)))
        while w >= v and v < size:
            w = w - v
            v = v + 1
        if v < size:
            edges.add((v, w))
    return Graph(size, edges)


def get_data_path(algorithm_name: str):
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents=True, exist_ok=True)
    return (directory / algorithm_name).with_suffix('.csv')

def run_benchmark(algorithm, size: int):
    graph = fast_generate_er_graph(size)
    result = algorithm(graph)
    return size, result



if __name__ == "__main__":
    args = parser.parse_args()
    data_path = get_data_path(args.algorithm)
    with open(data_path, 'a') as f:
        for s in [25, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]:
            for i in range(100):
                size, res = run_benchmark(GRAPH_ALGORITHMS[args.algorithm], s)
                f.write(f"{size} {res}\n")
