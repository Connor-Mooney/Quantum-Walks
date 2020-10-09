from GluedTrees import ReducedGluedTree, GluedTree
from QuantumWalk import QuantumWalk
import numpy as np

redg = ReducedGluedTree(3)

print(redg.adjacencyMatrix)
qw = QuantumWalk(redg)
print(qw.quantumWalkOperator)
#print(np.linalg.eigvals(qw.quantumWalkOperator))

#g = GluedTree(2)
#print(g.adjacencyMatrix)
#qw = QuantumWalk(g)
#print(qw.quantumWalkOperator)
#print("\n")
