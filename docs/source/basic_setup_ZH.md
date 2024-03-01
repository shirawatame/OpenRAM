### [Go Back](./index.md#table-of-contents)

# 基本设置
本页显示了使用OpenRAM生成SRAM的基本设置。



## 目录
1. [Dependencies](#dependencies)
1. [Anaconda](#anaconda)
1. [Docker](#docker-deprecated-use-anaconda-instead)
1. [Environment](#environment)
1. [Sky130 Setup](#sky130-setup)



## 依赖
一般来说，OpenRAM编译器的依赖关系很少:
+ Git
+ Make
+ Python 3.5 或更高
+ 各种Python包 (pip install -r requirements.txt)
+ Anaconda



## Anaconda
我们使用 Anaconda 包管理器来安装 OpenRAM 使用的工具。
您不必担心更新/安装这些工具。OpenRAM 在后
台安装 Anaconda （不影响任何现有的 Anaconda
你有的设置）。

您不需要手动激活/停用 Anaconda 环境。OpenRAM 内
存在运行工具之前和之后自动管理此功能。

OpenRAM 默认使用 Anaconda，但您可以通过设置
配置文件中的“use_conda = False”。然后，OpenRAM
已安装在您的系统上并可以使用。

您还可以告诉 OpenRAM 应该在哪里安装 Anaconda 或哪个 Anaconda
设置它应该使用。您可以像这样设置“$CONDA_HOME”变量:
```
export CONDA_HOME="/path/to/conda/setup"
```

> **注意**: 如果您希望安装 Anaconda 而不运行 OpenRAM（例如
> 运行不安装 Anaconda 的单元测试），可以运行：
> ```
> ./install_conda.sh
> ```

> **注意**: 您可以卸载 OpenRAM 的 Anaconda 安装
> 只需要删除 Anaconda 安装到的文件夹.您可以运行：
> ```
> rm -rf miniconda
> ```

> **注意**: 您可以使用以下命令更改工具的版本：
> ```
> source ./miniconda/bin/activate
> conda uninstall <tool>
> conda install -y -c vlsida-eda <tool>=<version>
> ```



## Docker容器 (deprecated, use Anaconda instead)
我们有一个docker安装方式 [docker setup](../../docker) 来运行 OpenRAM. 要使用这个, 您应该
运行:
```
cd OpenRAM/docker
make build
```
这必须运行一次，并且需要一段时间才能构建所有工具。如果您已经
安装了 OpenRAM 库，您还可以从
安装目录运行docker安装程序。



## 环境

如果你还没有安装OpenRAM库或者你想使用不同的OpenRAM安装，你可以设置两个环境变量:
+ `OPENRAM_HOME` 应该指向编译器源目录。
+ `OPENRAM_TECH` 应该指向一个或多个根技术目录(冒号
分离)。

如果您已经安装了库并设置了 `OPENRAM_HOME` ，那么库将使用
安装在 `OPENRAM_HOME` 路径上。

> 查看Python库 [Python library](./python_library.md#go-back) 的细节.

如果你没有这个库，你也应该把 `OPENRAM_HOME` 添加到你的
`PYTHONPATH`。如果您有库，则不需要这样做。

您可以将这些环境变量添加到您的`.bashrc`中:
```
export OPENRAM_HOME="$HOME/OpenRAM/compiler"
export OPENRAM_TECH="$HOME/OpenRAM/technology"
export PYTHONPATH=$OPENRAM_HOME
```

注意，如果您希望在编辑器中解析符号，您可能还需要
添加您使用的特定技术目录和任何自定义技术
模块也是如此。例如:
```
export PYTHONPATH="$OPENRAM_HOME:$OPENRAM_TECH/sky130:$OPENRAM_TECH/sky130/custom"
```

我们包含了[SCMOS] SCN4M\_SUBM， [FreePDK45]所需的技术文件。然而，
[SCMOS]仿真模型是通用的，应该用foundry模型代替。
你可以在这里得到完整的 [FreePDK45 PDK here][FreePDK45].



## Sky130 安装

要安装Sky130 [Sky130], 您可以运行:

```
cd $HOME/OpenRAM
make sky130-pdk
```

这将使用volare来获取PDK。

> **注意**: 如果您没有安装Magic，则需要在运行此命令之前安装并激活conda环境。你可以运行:
> ```
> ./install_conda.sh
> source miniconda/bin/activate
> ```

然后，您还必须安装 [Sky130] SRAM构建空间与适当的
通过运行以下命令将cell视图放入OpenRAM技术目录:

```
cd $HOME/OpenRAM
make sky130-install
```

您也可以从包安装目录中运行这些
OpenRAM库。

## GF180 安装

OpenRAM目前**不**支持gf180mcu生成SRAM。然而，支持gf180mcu的ROM生成作为实验功能。

没有必要安装gf180mcu PDK，因为所有必要的文件都已经在git库中了 `technology/gf180mcu/`.

如果您仍然希望安装PDK，可以运行 `make gf180mcu-pdk`.

[SCMOS]:    https://www.mosis.com/files/scmos/scmos.pdf
[FreePDK45]: https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[Sky130]:   https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git

