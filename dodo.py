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

from pyctdev import * # noqa: api
