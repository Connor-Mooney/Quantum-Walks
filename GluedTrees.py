import numpy as np


class Graph:
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
        pass

    def fill_bipartite_sets(self):
        pass
    
    def display(self):
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
        cycle_array = []
        for i in range (2**self.n-1, 2**self.n - 1 + 2**(self.n - 1)):
            # Making an array with every leaf of the 2nd tree twice
            cycle_array.append(i)
            cycle_array.append(i)
        j = 2**(self.n - 1) - 1
        while not len(cycle_array) == 0:
            # Assigning two of the leaves to each leaf.
            # This doesn't really work always, because it may re-pick the same leaf so that needs fixing
            # But as for now, we aren't using this class for our calculations, we can worry about that later
            temp = cycle_array.pop(np.random.randint(len(cycle_array)))
            self.adjacencyMatrix[int(np.floor(j)), temp] = 1
            self.adjacencyMatrix[temp, int(np.floor(j))] = 1
            j += 0.5

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
    """This is the class we'll probably be doing most of our analysis on"""
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
            if i%2 == 0:
                self.A.add(i)
            else:
                self.B.add(i)
