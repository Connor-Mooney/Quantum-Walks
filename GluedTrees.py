import numpy as np


class Graph:
    """
        This class gives an adjacency matrix formulation of a bipartite graph.
        
        Local Variables:
            n : some parameter needed to generate graph
            start_set: the set of the starting vertices for the walk
            marked_set: the set of the marked vertices for the walk
            A: one of the bipartite sets
            B: the other bipartite set
            adjacencyMatrix: the graph's adjacency matrix
    """
    def __init__(self, n, start_set: set, marked_set: set):
        self.n = n
        self.adjacencyMatrix = None
        self.fill_adjacency_matrix()
        self.A = set()
        self.B = set()
        self.start_set = start_set
        self.marked_set = marked_set
        self.fill_bipartite_sets()
        
    def fill_adjacency_matrix(self):
        """To be implemented in child classes. Populates adjacencyMatrix"""
        pass

    def fill_bipartite_sets(self):
        """To be implemented in child classes. Populates A and B."""
        pass
    
    def display(self):
        """Displays the adjacency matrix"""
        print(self.adjacencyMatrix)


class GluedTree(Graph):
    """This class gives full binary glued trees where each tree has depth n,
        and the leaves of each tree is connected to two leaves of the other tree randomly.
    """
    def __init__(self, n, start_set, marked_set):
        super().__init__(n, start_set, marked_set)

    def fill_adjacency_matrix(self):

        """ Fills out the adjacency matrix of a glued tree, labelling vertices by their number, starting at 0 with the
        top like so
                    0
                   / \
                  1   2
                 /\   /\
                3 4   5 6
                .
                .
                .
        And then doing the same for another tree, then gluing.
        """
        self.adjacencyMatrix = np.zeros((2*(2**self.n - 1), 2*(2**self.n - 1)))
        for i in range(2**(self.n-1)-1):
            # First we must find i's layer, which is layerNum
            layer_num = np.floor(np.log2(i+1))
            # Then we find where the next layer's nodes start off in numbering
            next_layer = 2**(layer_num + 1)-1
            # We then set the children of i to be adjacent to i
            self.adjacencyMatrix[i, int(next_layer + 2*(i-(2**layer_num - 1)))] = 1
            self.adjacencyMatrix[int(next_layer + 2*(i-(2**layer_num - 1))), i] = 1
            self.adjacencyMatrix[i, int(next_layer + 2*(i-(2**layer_num - 1)) + 1)] = 1
            self.adjacencyMatrix[int(next_layer + 2*(i-(2**layer_num - 1)) + 1), i] = 1
        for i in range(2**(self.n-1)-1):
            # We are essentially doing the same thing as
            # the above loop, but inverting the nodes to get a diamond-shaped configuration
            # First we must find i's layer, which is layerNum
            layer_num = np.floor(np.log2(i+1))
            # Then we find where the next layer's nodes start off in numbering
            next_layer = 2**(layer_num + 1)-1
            # We then set the children of i to be adjacent to i
            self.adjacencyMatrix[2*2**self.n - 3 - i, 2*2**self.n - 3 - int(next_layer + 2*(i-(2**layer_num - 1)))] = 1
            self.adjacencyMatrix[2*2**self.n - 3 - int(next_layer + 2*(i-(2**layer_num - 1))), 2*2**self.n - 3 - i] = 1
            self.adjacencyMatrix[2*2**self.n - 3 - i, 2*2**self.n - 3 - int(next_layer + 2*(i-(2**layer_num - 1)) + 1)] = 1
            self.adjacencyMatrix[2*2**self.n - 3 - int(next_layer + 2*(i-(2**layer_num - 1)) + 1), 2*2**self.n - 3 - i] = 1
        # Next comes making the cycle that actually "glues" the trees together
        for i in range(2**(self.n-1)-1, 2**self.n-1):
            # fills out the ``glue'' in a specific way (think |x| repeated over and over again)
            if i % 2 == 1:
                print(i)
                self.adjacencyMatrix[i, 2**(self.n-1) + i] = 1
                self.adjacencyMatrix[i, 2**(self.n-1) + i + 1] = 1
                self.adjacencyMatrix[2**(self.n-1) + i, i] = 1
                self.adjacencyMatrix[2**(self.n-1) + i + 1, i] = 1
            else:
                self.adjacencyMatrix[i, 2**(self.n-1) + i] = 1
                self.adjacencyMatrix[i, 2**(self.n-1) + i - 1] = 1
                self.adjacencyMatrix[2**(self.n-1) + i - 1, i] = 1
                self.adjacencyMatrix[2**(self.n-1) + i, i] = 1

        j = 2**(self.n - 1) - 1

    def fill_bipartite_sets(self):
        # Sorts the vertices into their bipartite sets, with the set alternating based on layer, with 0 in A
        for i in range(2**self.n-1):
            if int(np.log2(i+1))%2 == 0:
                self.A.add(i)
            else:
                self.B.add(i)
        for i in range(2**self.n - 1, 2*(2**self.n - 1)):
            if int(np.log2(2*(2**self.n - 1) - i)) % 2 == 0:
                self.B.add(i)
            else:
                self.A.add(i)
        

class ReducedGluedTree(Graph):
    """Generates a reduced glued tree, that is the glued tree projected onto the row spaces,
    which gives a directed line graph."""
    def __init__(self, n, start_set: set, marked_set: set):
        super().__init__(n, start_set, marked_set)

    def fill_adjacency_matrix(self):
        self.adjacencyMatrix = np.zeros((2*self.n, 2*self.n))
        for i in range(self.n-1):
            self.adjacencyMatrix[i, i+1] = 2
            self.adjacencyMatrix[i+1, i] = 1
        self.adjacencyMatrix[self.n-1, self.n]=2
        self.adjacencyMatrix[self.n, self.n-1]=2
        for i in range(self.n, 2*self.n-1):
            self.adjacencyMatrix[i, i+1] = 1
            self.adjacencyMatrix[i+1, i] = 2
            
    def fill_bipartite_sets(self):
        for i in range(2 * self.n):
            if i % 2 == 0:
                self.A.add(i)
            else:
                self.B.add(i)
