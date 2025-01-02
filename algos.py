import numpy as np
import random
import networkx as nx

class Algos:
    def __init__(self, graph):
        self.graph = graph
    
    def partition(self, vertices):
        half = len(vertices)//2
        return vertices[:half], vertices[half+1:]

    def coloring(self, vertices=None):
        if vertices is None:
            vertices = list(self.graph.nodes)  # Get nodes from the NetworkX graph

        if len(vertices) == 0:
            return []
        if len(vertices) == 1:
            return [vertices]

        # Partition the vertices
        left_graph, right_graph = self.partition(vertices)

        # Recursively color each partition
        independent_sets_left = self.coloring(left_graph)
        independent_sets_right = self.coloring(right_graph)

        # Merge the independent sets
        return self.mergeIndependentSets(independent_sets_left, independent_sets_right)

    def mergeIndependentSets(self, independent_sets1, independent_sets2):
        """Merge independent sets while ensuring no conflicts."""
        if not independent_sets1:
            return independent_sets2
        if not independent_sets2:
            return independent_sets1

        merged_sets = independent_sets1[:]
        for j_set in independent_sets2:
            for i_set in merged_sets:
                if self.canBeMerged(i_set, j_set):
                    i_set.extend(j_set)
                    break
            else:
                merged_sets.append(j_set)
        return merged_sets

    def canBeMerged(self, i_set, j_set):
        """Check if two sets can be merged into a larger independent set."""
        for u in i_set:
            for v in j_set:
                if self.graph.has_edge(u, v):  # Use NetworkX's `has_edge` method
                    return False
        return True
    def iterative_coloring(self):
        vertices = list(self.graph.nodes)
        # Applying iterative coloring by attempting to form independent sets
        independent_sets = []
        for u in vertices:
            # Try to place u in an existing independent set
            placed = False
            for set_i in independent_sets:
                if self.canBeMerged(set_i, [u]):
                    set_i.append(u)
                    placed = True
                    break
            # If u cannot be placed in any existing set, create a new independent set
            if not placed:
                independent_sets.append([u])

        return independent_sets
def generate_connected_graph(num_nodes, num_edges):
    # Start by creating a random tree (which is always connected)
    graph = nx.gnm_random_graph(num_nodes, num_nodes - 1)  # Generates a connected graph with num_nodes-1 edges (tree)
    
    # Add random edges
    while graph.number_of_edges() < num_edges:
        u, v = random.randint(0, num_nodes - 1), random.randint(0, num_nodes - 1)
        if u != v:
            graph.add_edge(u, v)
    
    return graph

# Example Usage
for i in range(0, 3):
    num_nodes = 1000  # Number of nodes
    num_edges = 10000  # Number of edges

    graph = generate_connected_graph(num_nodes, num_edges)
    
    algo = Algos(graph)
    my = algo.coloring()
    coloring = nx.coloring.greedy_color(graph, strategy='largest_first')
    
    # Print results: coloring sets and chromatic number (max color + 1)
    print("My algo: ", len(my))
    print("Greedy algorithm coloring result:", max(coloring.values()) + 1)
    print()

