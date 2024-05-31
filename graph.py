# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.

from collections.abc import Iterable

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]]):
		self.adj_list = {}
		self.edges = set()
		self.num_edges = 0
		self.num_nodes = num_nodes
		for i in range(num_nodes): # Adds all nodes to the adjacency list
			self.adj_list[i] = []
			
		for n1,n2 in edges:
			if n1 not in self.adj_list:
				self.adj_list[n1] = []
			if n2 not in self.adj_list:
				self.adj_list[n2] = []
			if n1 == n2:
				continue
			# The 3 previous conditions are for error checking
			edge = (min(n1,n2), max(n1,n2))  # Resolved duplicate edges
			if edge not in self.edges:
				self.adj_list[n1].append(n2)
				self.adj_list[n2].append(n1)
				self.edges.add(edge)
				self.num_edges += 1
		
	def get_num_nodes(self) -> int:
		return self.num_nodes

	def get_num_edges(self) -> int:
		return self.num_edges

	def get_neighbors(self, node: int) -> Iterable[int]:
		return self.adj_list[node]

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
