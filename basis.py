import itertools

from tqdm import tqdm

import numpy as np
import scipy as sp
import scipy.sparse as sparse
import matplotlib.pyplot as plt
from numpy import linalg as lin


class Basis():
    def get_arrangement(self, index):
        raise NotImplementedError
    def get_pair(self, index_1, index_2):
        raise NotImplementedError
    def get_num_raised(self, index):
        raise NotImplementedError
    # def get_flipped_arrangement_index(self, index, qubit):
    #     raise NotImplementedError
    # def get_flipped_arrangement(self, index, qubit):
    #     raise NotImplementedError

class Standard_Basis(Basis):
    def __init__(self, num_qubits = 2):
        self.num_qubits = num_qubits
        basis = {}
        for q, state in enumerate(itertools.product((0, 1), repeat = num_qubits)):
            basis[q] = state

        reverse_basis = {v: k for k, v in basis.items()}

        self.basis = basis
        self.reverse_basis = reverse_basis

    def get_arrangement(self, index):
        return self.basis[index]

    def get_pair(self, q_1, q_2):
        pair = []
        state_1, state_2 = self.basis[q_1], self.basis[q_2]
        oneup, onedown = 0, 0
        diffs = 0

        for i in range(0, self.num_qubits):
            if state_1[i] != state_2[i]:
                diffs += 1
                if diffs > 2:
                    return 0
                if (state_1[i] == 1)&(oneup == 0):
                    oneup = 1
                    pair.append(i)
                elif (state_1[i] == 0)&(onedown == 0):
                    onedown = 1
                    pair.append(i)
                else:
                    return 0
        if len(pair) < 2:
            return 0
        return pair

    def get_num_raised(self, index):
        m = 0
        for i in range(0, self.num_qubits):
            if self.get_arrangement(index)[i] == 1:
                m += 1
        return m






