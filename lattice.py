import numpy as np


class Lattice():
    def get_element_location(self, index):
        raise NotImplementedError
    def get_element_separation(self, index1, index2):
        raise NotImplementedError

class RandomLattice(Lattice):
    def __init__(self, num_qubits, dimension):
        self.num_qubits = num_qubits
        self.dimension = dimension
        self.lattice = []

        for i in range(0, num_qubits):
            position = []
            for x in range(0, dimension):
                position.append(np.random.rand())
            self.lattice.append(position)

    def get_element_location(self, index):
        return self.lattice[index]

    def get_element_separation(self, index1, index2):
        r1 = self.lattice[index1]
        r2 = self.lattice[index2]
        sep = 0
        for x in range(0, self.dimension):
            sep += np.power( r1[x] - r2[x], 2)
        return np.sqrt(sep)



