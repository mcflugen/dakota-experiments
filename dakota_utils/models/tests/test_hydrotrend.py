#!/usr/bin/env python
#
# Tests for dakota_utils.models.hydrotrend.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import *
import os
import tempfile
import shutil
from dakota_utils.models.hydrotrend import HydroTrend

nonfile = 'wvwbfb9vwvfnv.f'

def setup_module():
    print('HydroTrend tests:')
    os.environ['_test_hydrotrend_dir'] = tempfile.mkdtemp()

def teardown_module():
    shutil.rmtree(os.environ['_test_hydrotrend_dir'])

def test_HydroTrend_no_arguments():
    '''
    Tests whether no arguments creates input and output directories.
    '''
    os.chdir(os.environ['_test_hydrotrend_dir'])
    h = HydroTrend()
    assert_true(os.path.exists(h.input_dir))
    assert_true(os.path.exists(h.output_dir))

def test_HydroTrend_set_input_dir():
    '''
    Tests setting the input directory on init.
    '''
    os.chdir(os.environ['_test_hydrotrend_dir'])
    input_dir = '__hydro_in'
    h = HydroTrend(input_dir)
    assert_equal(h.input_dir, input_dir)

def test_HydroTrend_set_output_dir():
    '''
    Tests setting the output directory on init.
    '''
    os.chdir(os.environ['_test_hydrotrend_dir'])
    output_dir = '__hydro_out'
    h = HydroTrend(None, output_dir)
    assert_equal(h.output_dir, output_dir)

def test_load_no_output_file():
    '''
    Tests return from load() when no output file is defined.
    '''
    os.chdir(os.environ['_test_hydrotrend_dir'])
    h = HydroTrend()
    r = h.load()
    assert_is_none(r)



