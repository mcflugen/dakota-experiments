#! /usr/bin/env python
# Brokers communication between HydroTrend and Dakota through files.
# Mark Piper (mark.piper@colorado.edu)

import sys
import os
import re
import shutil
from subprocess import call
import numpy as np


def read(output_file):
    '''
    Reads a column of text containing HydroTrend output. Returns a numpy array.
    '''
    with open(output_file, 'r') as fp:
        values = fp.read().split('\n')

    return np.array(values[2:-1], dtype=np.float) # Remove header lines and EOF.


def write(results_file, array, labels=['Qs_mean', 'Qs_stdev']):
    '''
    Writes a Dakota results file from an input array.
    '''
    try:
        fp = open(results_file, 'w')
        for i in range(len(array)):
            fp.write(str(array[i]) + '\t' + labels[i] + '\n')
    except IOError:
        raise
    finally:
        fp.close()


def get_labels(params_file):
    '''
    Uses a regular expression to extract labels from a Dakota parameters file.
    '''
    labels = []
    try:
        fp = open(params_file, 'r')
        for line in fp:
            if re.search('ASV_', line):
                labels.append(''.join(re.findall(':(\S+)', line)))
    except IOError:
        raise
    finally:
        fp.close()
        return(labels)


# Files and directories.
start_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(start_dir, 'HYDRO_IN')
if not os.path.exists(input_dir): os.mkdir(input_dir)
output_dir = os.path.join(start_dir, 'HYDRO_OUTPUT')
if not os.path.exists(output_dir): os.mkdir(output_dir)
input_template = 'HYDRO.IN.template'
input_file = 'HYDRO.IN'
output_file = 'HYDROASCII.QS'

# Use the parsing utility `dprepro` (from $DAKOTA_DIR/bin) to
# incorporate the parameters from Dakota into the HydroTrend input
# template, creating a new HydroTrend input file.
shutil.copy(os.path.join(start_dir, input_template), os.curdir)
call(['dprepro', sys.argv[1], input_template, input_file])
shutil.copy(input_file, input_dir)

# Call HydroTrend, using the updated input file.
call(['hydrotrend', '--in-dir', input_dir, '--out-dir', output_dir])

# Calculate mean and standard deviation of Qs for the simulation
# time. Write the results to a Dakota results file.
shutil.copy(os.path.join(output_dir, output_file), os.curdir)
Qs = read(output_file)
m_Qs = [np.mean(Qs), np.std(Qs)]
labels = get_labels(sys.argv[1])
write(sys.argv[2], m_Qs, labels)
