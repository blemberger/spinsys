import numpy as np


class State():
    def __init__(self, coeffs = []):
        self.coeffs = []
        self.dim = len(coeffs)

        for q in range(0, len(coeffs)):
            self.coeffs.append(coeffs[q])


    @classmethod
    def random(cls, state_length):
        rand_vec = []
        norm = 0
        for q in range(0, state_length):
            rand_element = np.random.rand()*np.exp(2*np.pi*1j*np.random.rand())
            rand_vec.append(rand_element)
            norm += np.abs(rand_element)**2
        rand_vec = rand_vec/np.sqrt(norm)
        return cls(rand_vec)


    def get_norm(self):
        normsq = 0
        for q in range(0, len(self.coeffs)):
            normsq += np.abs(self.coeffs[q])**2
        return np.sqrt(normsq)







class Density():
    def __init__(self, matrix = [[.5,0],[0,.5]]):
        self.matrix = matrix
        # print(matrix)
        # print(len(matrix[0]))
        self.dim = len(matrix[0])

    @classmethod
    def from_state(cls, state):
        matrix = np.zeros([state.dim, state.dim], dtype = np.complex128)
        for q1 in range(0, state.dim):
            for q2 in range(0, state.dim):
                matrix[q1, q2] = state.coeffs[q1] * np.conj(state.coeffs[q2])
        return cls(matrix)

    @classmethod
    def random_product(cls, index):
        matrix = np.zeros([state.dim, state.dim], dtype=np.complex128)
        #make a product state
        return cls(matrix)



    def get_trace(self):
        trace = 0
        for q in range(0, self.dim):
            trace += self.matrix[q,q]**2
            if np.imag(self.matrix[q,q]) > .001:
                print('imaginary diagonal rho elements, something is fucked')


    def get_reduced(self, basis, qubit, r1, r2):
        result = 0
        for q in range(0, self.dim):
            if (r1 == 1) & (r2 == 1):
                if basis.get_arrangement(q)[qubit] == 1:
                    # print('assigned', self.matrix[q, q])
                    result += self.matrix[q, q]
                elif basis.get_arrangement(q)[qubit] != 0:
                    print('fuck')
            elif (r1 == 0) & (r2 == 0):
                if basis.get_arrangement(q)[qubit] == 0:
                    # print('assigned', self.matrix[q, q])
                    result += self.matrix[q, q]
                elif basis.get_arrangement(q)[qubit] != 1:
                    print('double fuck')
            elif r1 == r2:
                print('triple fuck')

        if (r1 == 1) & (r2 == 0):
            for q1 in range(0, self.dim):
                for q2 in range(0, self.dim):
                    if (basis.get_arrangement(q1)[qubit] == 1)&(basis.get_arrangement(q2)[qubit] == 0):
                        # print('assigned', self.matrix[q1, q2])
                        result += self.matrix[q1, q2]
        elif (r1 == 0) & (r2 == 1):
            for q1 in range(0, self.dim):
                for q2 in range(0, self.dim):
                    if (basis.get_arrangement(q1)[qubit] == 0)&(basis.get_arrangement(q2)[qubit] == 1):
                        # print('assigned', self.matrix[q1, q2])
                        result += self.matrix[q1, q2]
        # print('rho1:', result)
        return result