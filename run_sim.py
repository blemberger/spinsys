import os
import sys

import matplotlib
matplotlib.use('agg')

import simulacra as si

if __name__ == '__main__':
    spec_name = sys.argv[1]

    spec_path = os.path.join(os.getcwd(), f'{spec_name}.spec')
    sim = si.Specification.load(spec_path).to_sim()

    sim.run()

    sim.save()