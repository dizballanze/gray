#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup


def load_requirements(fname):
    """ load requirements from a pip requirements file """
    with open(fname) as f:
        line_iter = (line.strip() for line in f.readlines())
        return [line for line in line_iter if line and line[0] != "#"]


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

module_name = "gray"

readme = open("README.md").read()

history = open("HISTORY.md").read()

setup(
    name=module_name,
    version="0.8.0",
    description="Less uncompromising Python code formatter",
    long_description=f"{readme}\n\n{history}",
    long_description_content_type="text/markdown",
    author="Yuri Shikanov",
    author_email="dizballanze@gmail.com",
    url="https://github.com/dizballanze/gray",
    packages=find_packages(exclude=["tests"]),
    package_dir={module_name: module_name},
    include_package_data=True,
    install_requires=load_requirements("requirements.txt"),
    extras_require={"develop": load_requirements("requirements.dev.txt")},
    license="MIT",
    keywords="gray",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "console_scripts": [
            "{0} = {0}.main:main".format(module_name),
        ],
    },
)
