import simulacra as si
import numpy as np
from . import hamiltonian as ham
from . import state as sta
from . import basis as bas
from tqdm import tqdm
from copy import deepcopy


norm_tolerance = .1

class SpinSimulation(si.Simulation):
    def __init__(self, spec: 'SpinSpecification'):
        super().__init__(spec)
        self.times = np.linspace(
            0,
            self.spec.interval,
            int(self.spec.interval/self.spec.time_step),
        )
        state_data_shape = (len(self.times), self.spec.initial_state.dim)
        rho_data_shape = (len(self.times), self.spec.initial_state.dim, self.spec.initial_state.dim)
        rho1_data_shape = (len(self.times), 2, 2)

        self.state_vs_time = np.zeros(state_data_shape, dtype = np.complex128)
        self.rho_vs_time = np.zeros(rho_data_shape, dtype = np.complex128)
        self.rho1_vs_time = np.zeros(rho1_data_shape, dtype = np.complex128)

        self.state_vs_time[0] = spec.initial_state.coeffs
        initial_rho = sta.Density.from_state(sta.State(self.state_vs_time[0, :]))
        self.rho_vs_time[0] = initial_rho.matrix

        for r1 in range(0, 2):
            for r2 in range(0, 2):
                self.rho1_vs_time[0, r1, r2] = initial_rho.get_reduced(self.spec.basis, 0, r1, r2)

        print('init rho1', self.rho1_vs_time[0])



    def time_step(self, state, step, hamiltonian):
        change = np.zeros(len(state), dtype=np.complex128)
        for q1 in range(0, len(state)):
            delta_q1 = 0
            for q2 in range(0, len(state)):
                delta_q1 += hamiltonian.get_element(q1, q2) * state[q2]
            change[q1] = delta_q1
        result = state + 1j * self.spec.time_step * change
        return result






    def run(self):
        self.status = si.Status.RUNNING

        t_count = 1
        while t_count < len(self.state_vs_time):
            print(t_count/len(self.state_vs_time))
            current_state = self.state_vs_time[t_count - 1]
            self.state_vs_time[t_count] = self.time_step(self.state_vs_time[t_count - 1], self.spec.time_step, self.spec.hamiltonian)

            if np.abs(sta.State(self.state_vs_time[t_count]).get_norm() - 1) > norm_tolerance:
                print('norm drifting past tolerance')

            rho = sta.Density.from_state(sta.State(self.state_vs_time[t_count]))
            self.rho_vs_time[t_count] = rho.matrix

            for r1 in range(0, 2):
                for r2 in range(0, 2):
                    self.rho1_vs_time[t_count, r1, r2] = rho.get_reduced(self.spec.basis, 0, r1, r2)

            t_count += 1

        self.status = si.Status.FINISHED



class SpinSpecification(si.Specification):
    simulation_type = SpinSimulation

    def __init__(
            self,
            name: str,
            num_qubits: int,
            interval: float,
            time_step: float,
            initial_state: sta.State,
            hamiltonian: ham.Hamiltonian,
            basis: bas.Basis,
            **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.num_qubits = num_qubits
        self.interval = interval
        self.time_step = time_step
        self.initial_state = initial_state
        self.hamiltonian = hamiltonian
        self.basis = basis
