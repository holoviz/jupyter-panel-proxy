import pathlib

from glob import glob

import param as _param

exclude_patterns = ['setup.py', 'dodo.py', '.ipynb_checkpoints']

ICON_PATH = str((pathlib.Path(__file__).parent / "icons" / "logo.svg").absolute())

__version__ = str(
    _param.version.Version(
        fpath=__file__,
        archive_commit="$Format:%h$",
        reponame="panel_server",
))


def _discover_apps(filetypes=('py', 'ipynb')):
    base_dir = pathlib.Path(__file__).parent.parent
    example_dir = base_dir / 'examples'
    if example_dir.is_dir():
        base_path = example_dir
    else:
        base_path = base_dir
    apps = []
    for ft in filetypes:
        for app in base_path.glob(f'**/*.{ft}'):
            app = str(app)
            if not any(ep in app for ep in exclude_patterns):
                apps.append(app)
    return apps

def setup_panel_server():
    apps = _discover_apps()
    return {
        'command': ["panel", "serve", *apps, "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}panel", "--autoreload"],
        'absolute_url': True,
        'timeout': 360,
        "launcher_entry": {
            "enabled": True,
            "title": "Panel Launcher",
            "icon_path": ICON_PATH
        },
    }
