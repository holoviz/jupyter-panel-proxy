import fnmatch
import glob
import pathlib
import yaml

import param

__version__ = str(
    param.version.Version(
        fpath=__file__,
        archive_commit="$Format:%h$",
        reponame="panel_server",
))

EXCLUDE_PATTERNS = ['*setup.py', '*dodo.py', '*.ipynb_checkpoints*']

ICON_PATH = str((pathlib.Path(__file__).parent / "icons" / "logo.svg").absolute())

LAUNCHER_ENTRY = {
    "enabled": True,
    "title": "Panel Launcher",
    "icon_path": ICON_PATH
}

DEFAULT_CONFIG = {
    'autoreload': True,
    'file_types': ['ipynb', 'py'],
    'launcher_entry': LAUNCHER_ENTRY
}


def _get_config():
    config_path = pathlib.Path('jupyter-panel-proxy.yml')
    config = dict(DEFAULT_CONFIG)
    if config_path.is_file():
        with open(config_path) as f:
            config.update(yaml.load(f.read(), Loader=yaml.BaseLoader))
    return config


def _search_apps(config):
    base_dir = pathlib.Path('./')
    example_dir = base_dir / 'examples'
    if example_dir.is_dir():
        base_path = example_dir
    else:
        base_path = base_dir
    apps = []
    for ft in config.get('file_types'):
        apps += [str(app) for app in base_path.glob(f'**/*.{ft}')]
    return apps


def _discover_apps():
    config = _get_config()
    if 'apps' in config:
        found_apps = []
        for app_spec in config.get('apps', []):
            found_apps += glob.glob(app_spec)
    else:
        found_apps = _search_apps(config)
    exclude_patterns = config.get('exclude_patterns', []) + EXCLUDE_PATTERNS
    config['apps'] = [
        app for app in found_apps
        if not any(fnmatch.fnmatch(app, ep) for ep in exclude_patterns)
    ]
    return config


def _launch_command(port):
    config = _discover_apps()
    command = ["panel", "serve", *config.get('apps'), "--allow-websocket-origin=*", "--port", f"{port}", "--prefix", "{base_url}panel", "--disable-index-redirect"]
    if config.get('autoreload'):
        command.append('--autoreload')
    if config.get('warm'):
        command.append('--warm')
    if 'num_procs' in config:
        command += ['--num-procs', str(config['num_procs'])]
    if 'static_dirs' in config:
        command += ['--static-dirs', *config['static_dirs']]
    if 'oauth_provider' in config:
        from cryptography.fernet import Fernet
        from bokeh.util.token import generate_secret_key
        command += ['--oauth-provider', config['oauth_provider']]
        command += ['--oauth-encryption-key', Fernet.generate_key()]
        command += ['--cookie-secret', generate_secret_key()]
    if 'oauth_key' in config:
        command += ['--oauth-key', config['oauth_key']]    
    if 'oauth_secret' in config:
        command += ['--oauth-secret', config['oauth_secret']]
    if 'oauth_redirect_uri' in config:
        command += ['--oauth-redirect-uri', config['oauth_redirect_uri']]
    if 'oauth_jwt_user' in config:
        command += ['--oauth-jtw-user', config['oauth_jwt_user']]
    if 'oauth_extra_params' in config:
        command += ['--oauth-extra-params', repr(config['oauth_extra_params'])]
    if 'index' in config:
        command += ['--index', str(pathlib.Path(config['index']).absolute())]
    return command


def setup_panel_server():
    config = _get_config()
    spec = {
        'command': _launch_command,
        'absolute_url': True,
        'timeout': 360
    }
    if 'launcher_entry' in config:
        spec['launcher_entry'] = config['launcher_entry']
    return spec
