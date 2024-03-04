#!/usr/bin/env python3
# 有关许可信息，请参见LICENSE。
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
SRAM Compiler

输出文件将给定的后缀附加到输出名称后:
a spice (.sp) file for circuit simulation 用于电路仿真的spice (.sp)文件
a GDS2 (.gds) file containing the layout 包含布局的GDS2 (.gds)文件
a LEF (.lef) file for preliminary P&R (real one should be from layout) 用于初步P&R的LEF (. left)文件(真正的应该来自版图)
a Liberty (.lib) file for timing analysis/optimization 用于时间分析/优化的Liberty (.lib)文件
"""

import sys
import os
import datetime

# 如果您确定安装了openram包，则不需要接下来的两行
from common import *
make_openram_package()
import openram

(OPTS, args) = openram.parse_args()

# 检查是否只剩下一个配置文件作为参数。
if len(args) != 1:
    print(openram.USAGE)
    sys.exit(2)

# 设置top进程为openram
OPTS.top_process = 'openram'

# 这些依赖于参数，所以现在不要加载它们。
from openram import debug

# 解析配置文件并设置所有选项
openram.init_openram(config_file=args[0])

# Ensure that the right bitcell exists or use the parameterised one 确保存在正确的bitcell，或者使用参数化的bitcell
openram.setup_bitcell()

# 这里只打印banner，所以它不在单元测试中
openram.print_banner()

# 持续跟踪运行状态
start_time = datetime.datetime.now()
openram.print_time("Start", start_time)

# 输出本次运行的信息
openram.report_status()

debug.print_raw("Words per row: {}".format(OPTS.words_per_row))

output_extensions = ["lvs", "sp", "v", "lib", "py", "html", "log"]
# 如果后端只输出lef/gds
if not OPTS.netlist_only:
    output_extensions.extend(["lef", "gds"])

output_files = ["{0}{1}.{2}".format(OPTS.output_path,
                                    OPTS.output_name, x)
                for x in output_extensions]
debug.print_raw("Output files are: ")
for path in output_files:
    debug.print_raw(path)

# 创建一个SRAM(我们也可以传递sram_config，详细信息请参阅文档/教程)
from openram import sram
s = sram()

# 输出生成的SRAM的文件
s.save()

# 删除temp中的文件
openram.end_openram()
openram.print_time("End", datetime.datetime.now(), start_time)
