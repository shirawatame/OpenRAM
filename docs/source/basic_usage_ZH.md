### [Go Back](./index.md#table-of-contents)

# 基本用法
文档的这一页解释了OpenRAM的SRAM compiler的基本用法。 有关ROM编译器的使用，请参阅此处 [here](./basic_rom_usage.md#go-back)



## 目录表
1. [Environment Variable Setup](#environment-variable-setup-assuming-bash)
1. [Command Line Usage](#command-line-usage)
1. [Script Usage](#script-usage)
1. [Configuration Files](#configuration-files)
1. [Common Configuration File Options](#common-configuration-file-options)
1. [Output Files](#output-files)
1. [Data Sheets](#data-sheets)



## 环境变量设置 (假设是 bash)
> **注意**: 如果您有OpenRAM库此步骤可选. 
> 请看Python库 [Python library](./python_library.md#go-back) 的详细内容.
* `OPENRAM_HOME` 定义编译器目录的位置
    * `export OPENRAM_HOME="$HOME/openram/compiler"`
* `OPENRAM_TECH` 定义了技术存在的路径列表
    * `export OPENRAM_TECH="$HOME/openram/technology"`
    * 冒号分隔的列表，以便您可以拥有私有技术库
* 还必须有任何PDK相关的变量设置
* 添加编译器到 `PYTHONPATH`
    * `export PYTHONPATH="$PYTHONPATH:$OPENRAM_HOME"`



## 命令行用法
一旦定义了环境，就可以从命令行运行OpenRAM
使用一个用Python编写的配置文件。你可以运行OpenRAM
执行:
```
python3 $OPENRAM_HOME/../sram_compiler.py myconfig
```
你可以看到配置文件的所有选项在
$OPENRAM\_HOME/options.py

要运行宏，建议使用以下:
```
cd OpenRAM/macros
make example_config_scn4m_subm
```

* 常见参数:
    * `-h` 输出所有参数
    * `-t` 指定工艺技术 (scn4m\_subm 或 scmos 或 freepdk45)
    * `-v` 增加输出边幅
    * `-n` 不运行 DRC/LVS
    * `-c` 执行基于仿真的特性描述
    * `-d` 不清除 /tmp 目录下内容



## 脚本使用
OpenRAM也可以作为Python库使用。 请看Python库
[Python library](./python_library.md#go-back) 的详细内容.



## 配置文件
* 使用Python配置文件创建内存以复制结果
    * 无 YAML, JSON, etc.
* 完整的配置选项在 `$OPENRAM_HOME/options.py`
* 一些选项也可以在命令行上指定
    * 不建议用于复制结果
* 配置文件示例:
    ```python
    # Data word size 数据字长
    word_size = 2
    # Number of words in the memory 内存中单词数量
    num_words = 16

    # Technology to use in $OPENRAM_TECH 在$OPENRAM_TECH中使用的技术
    tech_name = "scn4m_subm"
    # Process corners to characterize 加工拐角来表征
    process_corners = [ "TT" ]
    # Voltage corners to characterize 电压角来表征
    supply_voltages = [ 3.3 ]
    # Temperature corners to characterize 温度角表征
    temperatures = [ 25 ]

    # Output directory for the results 结果的输出目录
    output_path = "temp"
    # Output file base name 输出文件名
    output_name = "sram_16x2"

    # Disable analytical models for full characterization (WARNING: slow!) 禁用完整表征的分析模型(警告:缓慢!)
    # analytical_delay = False

    # To force this to use magic and netgen for DRC/LVS/PEX 要强制使用魔法和netgen的DRC/LVS/PEX
    # Could be calibre for FreePDK45 可以为FreePDK45口径
    drc_name = "magic"
    lvs_name = "netgen"
    pex_name = "magic"
    ```



## 常用配置文件选项
* Characterization corners 描述角落
    * `supply_voltages = [1.7, 1.8, 1.9]`
    * `temperatures = [25, 50, 100]`
    * `process_corners = ["SS", "TT", "FF"]`
* Do not generate layout 不生成版图
    * `netlist_only = True`
* Multi-port options 多端口选项
    * `num_rw_ports = 1`
    * `num_r_ports = 1`
    * `num_w_ports = 0`
* Customized module or bit cell 自定义module或位cell
    * `bitcell = "bitcell_1rw_1r"`
    * `replica_bitcell = "replica_bitcell_1rw_1r"`
* Enable simulation characterization 启用仿真特性
    > **Warning**: Slow!
    * `analytical_delay = False`
* Output name and location 输出名字和位置
    * `output_path = "temp"`
    * `output_name = "sram_32x256"`
* Force tool selection (should match the PDK!) 强制工具选择(应该匹配PDK!)
    * `drc_name = "magic"`
    * `lvs_name = "netgen"`
    * `pex_name = "magic"`
* Include shared configuration options using Python imports 使用Python导入包括共享配置选项
    * `from corners_freepdk45 import *`



## 输出文件
输出文件放在配置文件中定义的 `output_dir` 中。

基本名称由 `output_name` 指定，并添加后缀。

最终结果文件如下:
* GDS (.gds)
* SPICE (.sp)
* Verilog (.v)
* P&R Abstract (.lef)
* Liberty (multiple corners .lib)
* Datasheet (.html)
* Log (.log)
* Configuration (.py) for replication of creation



## Data Sheets
![Datasheet 1](../assets/images/basic_usage/datasheet_1.png)
![Datasheet 2](../assets/images/basic_usage/datasheet_2.png)
![Datasheet 3](../assets/images/basic_usage/datasheet_3.png)
