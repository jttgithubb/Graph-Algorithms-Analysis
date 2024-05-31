# explanations for these functions are provided in requirements.py

from graph import Graph
from collections import defaultdict
import random

def get_diameter(graph: Graph) -> int:
	if not graph.adj_list:  # Empty adjacency lists have 0 diameter.
		return 0
	r = random.choice(list(graph.adj_list.keys()))
	max_dist = 0
	w, dist = graph.get_farthest_node_d(r)
	while (dist > max_dist):
		max_dist = dist
		r = w
		w, dist = graph.get_farthest_node_d(r)
	return max_dist


def get_clustering_coefficient(graph: Graph) -> float:
	denom = 0  # Calculate the number of 2-edge paths. 
	for node in graph.adj_list:
		node_deg = graph.get_degree(node)
		c_coeff = (node_deg * (node_deg-1)) / 2  
		denom += c_coeff
	triangle_cnt = 0  # Calculate the number of triangles using d-degeneracy.
	L, Nv, k = graph.get_degeneracy_order()
	for v in L:
		n = len(Nv[v])
		for i in range(n):
			for j in range(i+1, n):
				edge = (min(Nv[v][i], Nv[v][j]), max(Nv[v][i], Nv[v][j]))
				if edge in graph.edges:
					triangle_cnt += 1
	C = 3 * triangle_cnt / denom
	return C


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	deg_dict = defaultdict(int)
	dv = {v: len(neighbors) for v,neighbors in graph.adj_list.items()}
	for v in dv:
		deg_dict[dv[v]] += 1
	return deg_dict
