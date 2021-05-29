from glob import glob

import param as _param

__version__ = str(
    _param.version.Version(
        fpath=__file__,
        archive_commit="$Format:%h$",
        reponame="panel_server",
))

def setup_panel_server():
    return {
        'command': ["panel", "serve", *glob('./**/*.ipynb', recursive=True), *glob('./**/*.py', recursive=True), "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}panel", "--autoreload"],
        'absolute_url': True,
        'timeout': 360,
    }
