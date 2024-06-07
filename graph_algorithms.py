# explanations for these functions are provided in requirements.py

from graph import Graph
from collections import defaultdict
import random
import math

def get_diameter(graph: Graph) -> int:
	if not graph.adj_list:  # Empty adjacency lists have 0 diameter.
		return 0
	r = random.choice(list(graph.adj_list.keys()))
	max_dist = 0
	while (True):
		w, dist = graph.get_farthest_node_d(r)
		if dist > max_dist:
			max_dist = dist
			r = w
		else:
			break
	return max_dist
	'''num_nodes = graph.get_num_nodes()
	nodes = list(graph.adj_list.keys())
	farthest_nodes = set()
	init_samples = int(math.sqrt(num_nodes))
	final_samples = 200
	max_diameter = 0

	for i in range(init_samples):
		r = random.choice(nodes)
		w, dist = graph.get_farthest_node_d(r)
		if dist > max_diameter:
			max_diameter = dist
			farthest_nodes = set([w])
		elif dist == max_diameter:
			farthest_nodes.add(w)
	
	farthest_nodes = list(farthest_nodes)
	if len(farthest_nodes) > final_samples:
		farthest_nodes = random.sample(farthest_nodes, final_samples)
	for node in farthest_nodes:
		w, dist = graph.get_farthest_node_d(node)
		if dist > max_diameter:
			max_diameter = dist
	return max_diameter'''

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
