import numpy as np


class GluedTree:
    """This class gives full binary glued trees where each tree has depth n,
        and the leaves of each tree is connected to two leaves of the other tree randomly.
    """
    def __init__(self, n):
        self.n = n
        self.adjacencyMatrix = np.zeros((2*(2**n-1), 2*(2**n-1)))
        self.fill_adjacency_matrix()

    def fill_adjacency_matrix(self):

        """ Fills out the adjacency matrix of a glued tree, labelling vertices by their number, starting at 0 with the top like so
                    0
                   / \
                  1   2
                 /\   /\
                3 4   5 6
                .
                .
                .
        """
        for i in range(2**(self.n-1)-1):
            # First we must find i's layer, which is layerNum
            layer_num = np.floor(np.log2(i+1))
            # Then we find where the next layer's nodes start off in numbering
            next_layer = 2**(layer_num + 1)-1
            # We then set the children of i to be adjacent to i
            self.adjacencyMatrix[i,int(next_layer + 2*(i-(2**layer_num - 1)))] = 1
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
        for i in range (2**self.n-1, 2**self.n - 1 + 2**(self.n - 1)): #We're gonna make python array of length 2^(n-1)
            cycle_array.append(i)
            cycle_array.append(i)
        j = 2**(self.n - 1) - 1
        while(not cycle_array):
            temp = cycle_array.pop(np.randint(cycle_array.len()+1))
            self.adjacencyMatrix[j, temp] = 1
            self.adjacencyMatrix[temp, j] = 1
            j += 1

        print(self.adjacencyMatrix)

class ReducedGluedTree:
    """This is the class we'll probably be doing most of our analysis on"""
    def __init__(self, n):
