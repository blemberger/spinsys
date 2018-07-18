import argparse
import os
from pathlib import Path
import shutil
import subprocess

import numpy as np

import simulacra.cluster as clu

import spinsys

#test edit

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('job_name',
                        type = str,
                        help = 'the name of the job')
    parser.add_argument('--dir', '-d',
                        action = 'store', default = os.getcwd(),
                        help = 'directory to put the job directory in. Defaults to cwd')
    parser.add_argument('--overwrite', '-o',
                        action = 'store_true',
                        help = 'force overwrite existing job directory if there is a name collision')
    parser.add_argument('--dry',
                        action = 'store_true',
                        help = 'do not submit the job')

    args = parser.parse_args()

    args.job_dir = Path(args.dir) / args.job_name

    return args


def fmt_submit_string(args, specifications):
    with open('submit_template.sub') as f:
        submit_template = f.read()

    format_data = dict(
        batch_name = clu.ask_for_input('Job batch name?', default = args.job_name),
        memory = clu.ask_for_input('Memory (in MB)?', default = 100, cast_to = float),
        disk = clu.ask_for_input('Disk (in GB)?', default = 5, cast_to = float),
        num_jobs = len(specifications),
    )

    return submit_template.format(**format_data)


def check_for_possible_overwrite(args):
    if not args.job_dir.exists():
        return

    if args.overwrite:
        return

    if not clu.ask_for_bool('A job with that name already exists. Overwrite?', default = 'No'):
        clu.abort_job_creation()


def write_specs(job_dir, specifications):
    """Create the directories"""
    clu.save_specifications(specifications, job_dir)


def write_submit_file(job_dir, submit_string):
    """Write the submit string to a file."""
    print('Writing submit file...')
    with (job_dir / 'submit_job.sub').open(mode = 'w', encoding = 'utf-8') as file:
        file.write(submit_string)


def submit_job(job_dir):
    """Submit a job using a pre-existing submit file."""
    print('Submitting job...')
    os.chdir(job_dir)
    subprocess.run(('condor_submit', 'submit_job.sub'))
    os.chdir('..')


if __name__ == '__main__':
    args = parse_args()

    check_for_possible_overwrite(args)

    num_qubits = clu.Parameter(
        'number_of_qubits',
        clu.ask_for_input('number of qubits?', default = 'np.linspace(2, 4, 3)', cast_to = int),
        expandable = True,
    )
    spatial_dim = clu.Parameter(
        'number_of_spatial_dimensions',
        clu.ask_for_input('number of spatial dimensions?', default = 2, cast_to = int),
    )
    hamil_exp = clu.Parameter(
        'coupling_exponent',
        clu.ask_for_input('exponent for pairwise coupling?', default = -1, cast_to = float),
    )
    hamil_diagscale = clu.Parameter(
        'diagonal_scaling',
        clu.ask_for_input('diagonal scaling?', default = 1, cast_to = float),
    )
    hamil_offdiagscale = clu.Parameter(
        'odddiagonal_scaling',
        clu.ask_for_input('off-diagonal scaling?', default = 1, cast_to = float),
    )
    interval = clu.Parameter(
        'interval',
        clu.ask_for_input('end time?', default = .1, cast_to = float),
    )
    time_step = clu.Parameter(
        'time_step',
        clu.ask_for_input('time step?', default = .01, cast_to = float),
    )

    parameters = [num_qubits, spatial_dim, hamil_exp, hamil_diagscale, hamil_offdiagscale, interval, time_step]
    expanded_parameters = clu.expand_parameters(parameters)

    print('Generating specifications...')
    specifications = []
    for job_number, params in enumerate(expanded_parameters):
        spatial_dim = params['spatial_dim']
        hamil_exp = params['hamil_exp']
        hamil_diagscale = params['hamil_diagscale']
        hamil_offdiagscale = params['hamil_offdiagscale']
        num_qubits = params['num_qubits']

        basis = spinsys.bas.Standard_Basis(num_qubits)
        lattice = spinsys.lat.Random_Lattice(num_qubits, spatial_dim)



        spec = spinsys.SpinSpecification(
            name = str(job_number),
            initial_state = spinsys.sta.random_product(0),
            hamiltonian = spinsys.ham.Pairwise(basis, lattice, hamil_exp, hamil_diagscale, hamil_offdiagscale),
            basis = basis,
            **params,
        )

        specifications.append(spec)
    print(f'Generated {len(specifications)} specifications')

    submit_string = fmt_submit_string(args, specifications)
    print('\n' + submit_string + '\n')
    if not clu.ask_for_bool('Does the submit file look correct?', default = 'No'):
        clu.abort_job_creation()

    shutil.rmtree(args.job_dir, ignore_errors = True)  # ensure blank slate before writing anything
    clu.create_job_subdirs(args.job_dir)

    write_specs(args.job_dir, specifications)
    write_submit_file(args.job_dir, submit_string)

    if not args.dry:
        submit_job(args.job_dir)