from GluedTrees import ReducedGluedTree, GluedTree
from QuantumWalk import QuantumWalk
import numpy as np
from heapq import nsmallest
from matplotlib import pyplot as plt

def eff_res(n):
    r = 0
    for i in range(n):
        r += 2.*2.**(-i)
    r += 2.**(-n)
    return r


phase_gaps = []
num_qubits = []
for i in range(3, 100):
    #print("{}%".format(i))
    psi_s = np.zeros((2*i+1, 1))
    psi_s[0] = 1
    redg = ReducedGluedTree(i, {0}, {2*i-1})
    qw = QuantumWalk(redg, eff_res(i), eff_res(i))
    eigvals, eigvects = np.linalg.eig(qw.quantumWalkOperator)
    phases = np.imag(np.log(eigvals))
    phase_gap = nsmallest(2, np.abs(phases))[1]
    #print(phase_gap)
    #NOTE: This estimation of overlap seems to be FAULTY!!!!!
    phase_gaps.append(np.absolute(eigvects[list(phases).index(phase_gap)].dot(psi_s)))
    num_qubits.append(2*i)
plt.plot(num_qubits, phase_gaps)
#plt.title("Phase gap vs. number of edges")
#plt.ylabel("Phase gap of quantum walk operator")
#plt.xlabel("Number of edges")
plt.show()

#g = GluedTree(2)
#print(g.adjacencyMatrix)
#qw = QuantumWalk(g)
#print(qw.quantumWalkOperator)
#print("\n")

