import numpy as np
import matplotlib.pyplot as plt

# importing qiskit
from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

from GluedTrees import Graph

class QuantumWalk:
    def __init__(self, g, eta, x):
        self.g = g
        self.modifiedAdjacencyMatrix = None
        self.set_up_modified_adjacency_matrix(eta, x)
        self.quantumWalkOperator = None
        self.edge_list = []
        self.set_up_quantum_walk_operator()

    # Need to rejigger this to work with G' rather than G
    # I think it has been sufficiently modified
    def set_up_quantum_walk_operator(self):
        # Here we're going to set up the edge space and then make R_BR_A
        for i in range(list(self.modifiedAdjacencyMatrix.shape)[0]):
            for j in range(i, list(self.modifiedAdjacencyMatrix.shape)[1]):
                if self.modifiedAdjacencyMatrix[i, j] > 0:
                    self.edge_list.append({i, j})
        # Now time to create the quantum walk operators
        R_B = np.identity(len(self.edge_list), dtype=np.complex128)
        R_A = np.identity(len(self.edge_list), dtype=np.complex128)
        # This generates R_B and R_A for general bipartite graphs
        #print(self.g.B)
        for i in range(np.shape(self.modifiedAdjacencyMatrix)[0]):

            if i-1 in self.g.B or i == 0:
                R_B += self.diffuser(i)
            else:
                R_A += self.diffuser(i)
        # Setting the quantum walk operator to be R_AR_B
       # print("R_B: \n")
        #print(np.array2string(np.round(R_B, 3), max_line_width=np.infty))
        #print("\n R_A: \n")
        #print(np.array2string(np.round(R_A, 3), max_line_width=np.infty))

        self.quantumWalkOperator = R_A.dot(R_B)

    def diffuser(self, vertex):
        # we need to define ket_psi_v
        ket_psi_v = np.zeros((len(self.edge_list), 1), dtype=np.complex128)
        # Filling out ket_psi_v on the subspace we want
        for e in self.edge_list:
            if vertex in e:
                (other_vertex, ) = e.difference({vertex})
                ket_psi_v[self.edge_list.index(e), 0] = np.sqrt(self.modifiedAdjacencyMatrix[vertex, other_vertex])
        ket_psi_v = ket_psi_v / np.linalg.norm(ket_psi_v, 2)
        if not vertex == 0 and not vertex == np.shape(self.modifiedAdjacencyMatrix)[0]-1:
            print(ket_psi_v)
            return -2 * ket_psi_v.dot(ket_psi_v.T)
        else:
            return np.zeros((len(self.edge_list), len(self.edge_list)))

    def set_up_modified_adjacency_matrix(self, eta, x):
        # Sets up the modified adjacency matrix of G' according to Piddock's protocol in section 4
        # Notice how this only works for uniform initial distributions. That could be changed later if necessary
        self.modifiedAdjacencyMatrix = np.zeros((np.shape(self.g.adjacencyMatrix)[0]+2, np.shape(self.g.adjacencyMatrix)[1]+2))
        for i in range(1, np.shape(self.g.adjacencyMatrix)[0]+1):
            for j in range(1, np.shape(self.g.adjacencyMatrix)[0]+1):
                self.modifiedAdjacencyMatrix[i, j] = self.g.adjacencyMatrix[i-1, j-1]
        for s in self.g.start_set:
            self.modifiedAdjacencyMatrix[0, s+1] = np.sqrt(len(self.g.start_set))/eta
            self.modifiedAdjacencyMatrix[s+1, 0] = np.sqrt(len(self.g.start_set))/eta
        for m in self.g.marked_set:
            self.modifiedAdjacencyMatrix[-1, m+1] = 1/x
            self.modifiedAdjacencyMatrix[m+1, -1] = 1/x
       # print(np.array2string(self.modifiedAdjacencyMatrix, max_line_width=np.infty))

    def phase_estimation(self, ancilla_bits, starting_state):
        # need to think this through
        phase_estimator = QuantumCircuit(ancilla_bits + 2**np.ceiling(np.log2(len(self.edge_list))), ancilla_bits)
        # Initialise starting state

        # Run through
        phase_estimator.draw()
