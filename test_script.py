import numpy as np
import simulacra as si



from spinsys import sims as sims
from spinsys import state as sta
from spinsys import hamiltonian as ham
from spinsys import basis as bas
from spinsys import lattice as lat


N = 7
dim = 2
power = -2
stdbasis = bas.Standard_Basis(N)
rlattice = lat.RandomLattice(N, dim)
hamil = ham.Pairwise(stdbasis, rlattice, power)




spec = sims.SpinSpecification(
    'Spin System Test',
    num_qubits = N,
    interval = 4e-4,
    time_step = 1e-4,
    initial_state = sta.State.random(np.power(2, N)),
    basis = stdbasis,
    lattice = rlattice,
    hamiltonian = hamil,
)

sim = spec.to_sim()
sim.run()

spec.save('~/')


si.vis.xy_plot(
    'amplitude magnitude index 0',
    sim.times,
    np.real( sim.rho1_vs_time[:, 0, 1] ),
    x_label = r'$t$',
    y_label = r'$c_0$',
    title = 'rho01 for qubit indexed 0',
    show = False,
    save = True,
    img_format = 'png'
)