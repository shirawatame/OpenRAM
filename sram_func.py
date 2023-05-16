#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This script will functionally simulate an SRAM previously generated by OpenRAM
given a configuration file. Configuration option "use_pex" determines whether
extracted or generated spice is used. Command line arguments dictate the
number of cycles and period to be simulated.
"""

import sys
import datetime
from globals import *

# You don't need the next two lines if you're sure that openram package is installed
from common import *
make_openram_package()
import openram

(OPTS, args) = openram.parse_args()

# Override the usage
USAGE = "Usage: {} [options] <config file> <sp_file> <cycles> <period>\nUse -h for help.\n".format(__file__)

# Check that we are left with a single configuration file as argument.
if len(args) != 4:
    print(USAGE)
    sys.exit(2)

OPTS.top_process = 'memfunc'

# Parse argument
config_file = args[0]
sp_file = args[1]
cycles = int(args[2])
period = float(args[3])

# These depend on arguments, so don't load them until now.
from openram import debug

# Parse config file and set up all the options
openram.init_openram(config_file=config_file, is_unit_test=False)

openram.print_banner()

# Configure the SRAM organization (duplicated from openram.py)
from characterizer.fake_sram import fake_sram
s = fake_sram(name=OPTS.output_name,
              word_size=OPTS.word_size,
              num_words=OPTS.num_words,
              write_size=OPTS.write_size,
              num_banks=OPTS.num_banks,
              words_per_row=OPTS.words_per_row,
              num_spare_rows=OPTS.num_spare_rows,
              num_spare_cols=OPTS.num_spare_cols)

s.generate_pins()
s.setup_multiport_constants()

OPTS.netlist_only = True
OPTS.check_lvsdrc = False

# Generate stimulus and run functional simulation on the design
start_time = datetime.datetime.now()
from openram.characterizer import functional
debug.print_raw("Functional simulation... ")
f = functional(s, cycles=cycles, spfile=sp_file, period=period, output_path=OPTS.openram_temp)
(fail, error) = f.run()
debug.print_raw(error)
openram.print_time("Functional simulation", datetime.datetime.now(), start_time)

# Delete temp files, remove the dir, etc. after success
if fail:
    openram.end_openram()
