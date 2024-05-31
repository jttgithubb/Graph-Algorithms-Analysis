# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.

from collections.abc import Iterable
from collections import deque, defaultdict

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

	def get_degree(self, node):
		if node in self.adj_list:
			return len(self.adj_list[node])
		else:
			return 0
		
	def get_farthest_node_d(self, node):
		visited = set()
		queue = deque([(node, 0)])
		farthest_node = node
		max_dist = 0
		while queue:
			curr_node, dist = queue.popleft()
			visited.add(curr_node)
			for neighbor in self.adj_list[curr_node]:
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append((neighbor, dist + 1))
					if dist + 1 > max_dist:
						max_dist = dist + 1
						farthest_node = neighbor
		return farthest_node, max_dist
	
	def get_degeneracy_order(self):
		L = []
		L_set = set()  # Track nodes in L.
		n = self.get_num_nodes()
		dv = {v: len(neighbors) for v,neighbors in self.adj_list.items()}
		D = defaultdict(list)
		for v, degree in dv.items():
			D[degree].append(v)
		Nv = defaultdict(list)
		k = 0
		for node in range(n):
			i = 0
			while i not in D or not D[i]:
				i += 1
			k = max(k, i)
			v = D[i].pop()
			L.insert(0, v)
			L_set.add(v)
			for w in self.get_neighbors(v):
				if w not in L_set:
					old_deg = dv[w]
					new_deg = old_deg - 1
					dv[w] = new_deg
					D[old_deg].remove(w)
					D[new_deg].append(w)
					Nv[v].append(w)
		return L, Nv, k
	
	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
