#!/bin/bash
CONDA_INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-py38_23.11.0-2-Linux-x86_64.sh"
CONDA_INSTALLER_FILE="miniconda_installer_py38.sh"
CONDA_HOME="${CONDA_HOME:-miniconda}"

# 工具名称格式为 "<tool>=<version>" 。
# 如果你想使用最新版本, 那么使用 "<tool>"。
TOOLS=""
TOOLS+="klayout=0.28.3 "
TOOLS+="magic=8.3.363 "
TOOLS+="netgen=1.5.253 "
TOOLS+="ngspice=26 "
TOOLS+="trilinos=12.12.1=1 "
TOOLS+="xyce=7.4=3"

# 如果尚未安装miniconda请安装
if [[ ! -d "${CONDA_HOME}/bin" ]]
then
    curl -s -o ${CONDA_INSTALLER_FILE} ${CONDA_INSTALLER_URL}
    /bin/bash ${CONDA_INSTALLER_FILE} -b -p ${CONDA_HOME}
    rm ${CONDA_INSTALLER_FILE}
    source ${CONDA_HOME}/bin/activate

    # 对通道进行优先排序以防止版本冲突
    conda config --add channels conda-forge
    conda config --add channels vlsida-eda

    # 从conda-eda安装iverilog
    conda install -q -y -c litex-hub iverilog

    # 从vlsida-eda安装其余的工具
    for tool in ${TOOLS}
    do
        conda install -q -y -c vlsida-eda ${tool}
    done

    # 安装所需Python依赖包
    # (此步骤不是必需的，但用于防止可能出现的问题)
    python3 -m pip install -r requirements.txt --ignore-installed

    conda deactivate
fi

