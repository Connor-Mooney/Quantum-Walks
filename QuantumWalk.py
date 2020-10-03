import numpy as np
import qiskit
from GluedTrees import Graph


class QuantumWalk:
    def __init__(self, g):
        self.g = g
        self.quantumWalkOperator = None
        self.edge_list = []
        self.set_up_quantum_walk_operator()

    def set_up_quantum_walk_operator(self):
        # Here we're going to set up the edge space and then make R_BR_A
        # Notice this is only going to be set up to work properly for the reduced glued tree
        for i in range(list(self.g.adjacencyMatrix.shape)[0]):
            for j in range(i, list(self.g.adjacencyMatrix.shape)[1]):
                if self.g.adjacencyMatrix[i, j] > 0:
                    self.edge_list.append({i, j})
        # Now time to create the quantum walk operators
        R_B = np.zeros((len(self.edge_list), len(self.edge_list)))
        R_A = np.zeros((len(self.edge_list), len(self.edge_list)))
        # This relies on the properties of a reduced glued tree
        for i in range(2 * self.g.n):
            if i%2 == 1:
                R_B += self.diffuser(i)
            else:
                R_A += self.diffuser(i)
        # Setting the quantum walk operator to be R_AR_B
        self.quantumWalkOperator = R_A.dot(R_B)

    def diffuser(self, vertex):
        # we need to define ket_psi_v
        ket_psi_v = np.zeros((len(self.edge_list), 1))
        identity_support_v_vect = np.zeros((len(self.edge_list), 1))
        # Filling out ket_psi_v and the identity on the subspace we want
        for e in self.edge_list:
            if vertex in e:
                iter_e = iter(e)
                ket_psi_v[self.edge_list.index(e), 0] = np.sqrt(self.g.adjacencyMatrix[next(iter_e), next(iter_e)])
                identity_support_v_vect[self.edge_list.index(e), 0] = 1
        ket_psi_v = ket_psi_v / np.linalg.norm(ket_psi_v, 2)
        if not vertex == 0 and not vertex == self.g.n*2 - 1:
            return identity_support_v_vect.dot(identity_support_v_vect.T) - 2 * ket_psi_v.dot(ket_psi_v.T)
        else:
            return identity_support_v_vect.dot(identity_support_v_vect.T)

    def phase_estimation(self, ancilla_bits, starting_state):
        # need to think this through