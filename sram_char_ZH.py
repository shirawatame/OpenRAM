#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This script will characterize an SRAM previously generated by OpenRAM given a
configuration file. Configuration option "use_pex" determines whether extracted
or generated spice is used and option "analytical_delay" determines whether
an analytical model or spice simulation is used for characterization.
"""

import sys
import datetime

# 如果您确定安装了openram包，则不需要接下来的两行
from common import *
make_openram_package()
import openram

(OPTS, args) = openram.parse_args()

# Override the usage 覆盖用法
USAGE = "Usage: {} [options] <config file> <spice netlist>\nUse -h for help.\n".format(__file__)

# 检查是否只剩下一个配置文件作为参数。
if len(args) != 2:
    print(USAGE)
    sys.exit(2)

OPTS.top_process = 'memchar'

# 这些依赖于参数，所以现在不要加载它们。
from openram import debug

# 解析配置文件并设置所有选项
openram.init_openram(config_file=args[0], is_unit_test=False)

openram.print_banner()

# 配置SRAM组织(从sram_compiler.py复制)
from openram.characterizer import fake_sram
s = fake_sram(name=OPTS.output_name,
              word_size=OPTS.word_size,
              num_words=OPTS.num_words,
              write_size=OPTS.write_size,
              num_banks=OPTS.num_banks,
              words_per_row=OPTS.words_per_row,
              num_spare_rows=OPTS.num_spare_rows,
              num_spare_cols=OPTS.num_spare_cols)

debug.check(os.path.exists(args[1]), "Spice netlist file {} not found.".format(args[1]))
sp_file = args[1]
s.generate_pins()
s.setup_multiport_constants()

OPTS.netlist_only = True
OPTS.check_lvsdrc = False
OPTS.nomimal_corner_only = True

# TODO: remove this after adding trimmed netlist gen to sram run 在将修剪过的网表代添加到ram运行后删除此错误
OPTS.trim_netlist = False

# 设计特点
start_time = datetime.datetime.now()
from openram.characterizer import lib
debug.print_raw("LIB: Characterizing... ")
lib(out_dir=OPTS.output_path, sram=s, sp_file=sp_file, use_model=False)
print_time("Characterization", datetime.datetime.now(), start_time)

# 输出本次运行的信息
print("Output files are:\n{0}*.lib".format(OPTS.output_path))
#report_status() #could modify this function to provide relevant info 是否可以修改此函数以提供相关信息

# 删除temp文件(临时文件)，删除目录等
openram.end_openram()
