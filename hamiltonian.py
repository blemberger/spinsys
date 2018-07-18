import numpy as np

class Hamiltonian():
    def get_element(self, q1, q2):
        raise NotImplementedError

class Simple_Ham(Hamiltonian):
    def __init__(self, freq = 1):
        self.freq = freq

    def get_element(self, q1, q2):
        if q1 == q2:
            return self.freq
        else:
            return 0

    def __repr__(self):
        return f'{self.__class__.name__}(freq = {self.freq})'






class Pairwise(Hamiltonian):
    def __init__(self, basis, lattice, exponent = -1, diag_scale = 1, offdiag_scale = 1):
        self.exponent = exponent
        self.basis = basis
        self.num_qubits = basis.num_qubits
        self.dim = np.power(2, self.num_qubits)

        self.matrix = np.zeros([self.dim, self.dim])

        for q1 in range(0, self.dim):
            for q2 in range(q1 + 1, self.dim):
                pair = basis.get_pair(q1, q2)
                if pair != 0:
                    r = lattice.get_element_separation(pair[0], pair[1])
                    element = offdiag_scale * np.sin(np.random.rand()*2*np.pi)*np.power(r, self.exponent)
                    self.matrix[q1, q2] = element
                    self.matrix[q2, q1] = element
                if q1 == q2:
                    self.matrix[q1, q1] = diag_scale * basis.get_num_raised(q1)

    def get_element(self, q1, q2):
        return self.matrix[q1, q2]






