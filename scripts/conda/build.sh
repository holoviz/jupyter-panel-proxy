#!/usr/bin/env bash

set -euxo pipefail

MODULE="panel_server"
PACKAGE="jupyter-panel-proxy"

python -m build --sdist .

VERSION=$(python -c "import $MODULE; print($MODULE._version.__version__)")
export VERSION

conda build scripts/conda/recipe --no-anaconda-upload --no-verify -c conda-forge --package-format 1

mv "$CONDA_PREFIX/conda-bld/noarch/$PACKAGE-$VERSION-py_0.tar.bz2" dist
