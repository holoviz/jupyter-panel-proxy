"""
This file provides a mechanism to map between the semantic commands that any
project has (build docs, run tests, copy examples ... ) and the specific
command that should be run.

Most of these commands are stored in pyctdev which is essentially a collection
of the pyviz way of doing these actions. Commands that are newer, or specific
to a particular project, will live in this file instead. To see a list of
all the available commands - after installing pyctdev - run:

$ doit list
"""

import os

if "PYCTDEV_ECOSYSTEM" not in os.environ:
    os.environ["PYCTDEV_ECOSYSTEM"] = "conda"

from pyctdev import * # noqa: api

def task_pip_on_conda():
    """Experimental: provide pip build env via conda"""
    return {'actions':[
        # some ecosystem=pip build tools must be installed with conda when using conda...
        'conda install -y pip twine wheel',
        # ..and some are only available via conda-forge
        'conda install -y -c conda-forge tox virtualenv',
    ]}
