# 有关许可信息，请参见LICENSE。
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from setuptools import setup, find_namespace_packages


# 从repo的根目录将这些文件夹作为子模块包含
include = ["compiler", "docker", "technology", "macros"]
# 排除带有这些单词的文件/文件夹
exclude = ["docs", "images", "miniconda"]


# 找到' compiler '文件夹中的所有模块
dirs = []
for dir in find_namespace_packages():
    if any(x in dir for x in exclude):
        continue
    dirs.append(dir)

# 将' compiler '替换为' openram '作为包名
packages = []
for dir in dirs:
    packages.append(dir)

# 使包含的文件夹成为openram包的子模块
for i in range(len(packages)):
    if any(x in packages[i] for x in include):
        packages[i] = "openram." + packages[i]

# 修复目录路径
for i in range(len(dirs)):
    dirs[i] = dirs[i].replace(".", "/")

# 插入根作为openram模块
packages.insert(0, "openram")
dirs.insert(0, "")

# Zip package names and their paths
package_dir = {k: v for k, v in zip(packages, dirs)}


# 创建所需包的列表
with open("requirements.txt") as f:
    reqs = f.read().splitlines()


# 从文件中读取version
version = open("VERSION", "r").read().rstrip()


with open("README.md") as f:
    long_description = f.read()


# 调用安装程序来创建包
setup(
    name="openram",
    version=version,
    description="An open-source static random access memory (SRAM) compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://openram.org/",
    download_url="https://github.com/VLSIDA/OpenRAM/releases",
    project_urls={
        "Bug Tracker": "https://github.com/VLSIDA/OpenRAM/issues",
        "Documentation": "https://github.com/VLSIDA/OpenRAM/blob/stable/docs/source/index.md",
        "Source Code": "https://github.com/VLSIDA/OpenRAM",
    },
    author="Matthew Guthaus",
    author_email="mrg+vlsida@ucsc.edu",
    keywords=[ "sram", "magic", "gds", "netgen", "ngspice", "netlist" ],
    license="BSD 3-Clause",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: System :: Hardware",
    ],
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    install_requires=reqs,
)
