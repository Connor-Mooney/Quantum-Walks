import numpy as np
import qiskit
from GluedTrees import Graph


class QuantumWalk:
    def __init__(self, g):
        self.g = g
        self.quantumWalkOperator = None
        self.set_up_quantum_walk_operator()

    def set_up_quantum_walk_operator(self):
        # Here we're going to set up the edge space and then make R_BR_A
        # Notice this is only going to be set up to work properly for the reduced glued tree
        edge_list = []
        for i in range(self.g.adjacencyMatrix.shape()[0]):
            for j in range(i,self.g.adjacencyMatrix.shape()[1]):
                if self.g.adjacencyMatrix[i, j] > 0:
                    edge_list.append({i, j})
    # We need to make a mapping of labels of the vertices to labels of the edges in some way

    def diffuser(self, vertex, edge_list):
        # we need to define ket_psi_v =
        ket_psi_v = np.zeros((1, len(edge_list)))
        for e in edge_list:
            if e.contains(vertex):
                ket_psi_v[edge_list.index(e)] = np.sqrt(self.g.adjacencyMatrix[next(iter(e)), next(iter(e))])
        ket_psi_v = ket_psi_v / np.linalg.norm(ket_psi_v, 2)
        if not vertex == 0 and not vertex == self.g.n*2:
            return np.identity(len(edge_list)) - 2 * np.matmul(np.transpose(ket_psi_v), ket_psi_v)
            # this isn't quite it we need to make it such that the identities are
        else:
            return np.identity(len(edge_list))