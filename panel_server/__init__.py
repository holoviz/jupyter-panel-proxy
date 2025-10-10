import fnmatch
import glob
import os
import pathlib

import yaml

from .__version import __version__  # noqa: F401

EXCLUDE_PATTERNS = ['*setup.py', '*dodo.py', '*.ipynb_checkpoints*']

ICON_PATH = str((pathlib.Path(__file__).parent / "icons" / "logo.svg").absolute())

LAUNCHER_ENTRY = {
    "enabled": True,
    "title": "Panel Launcher",
    "icon_path": ICON_PATH
}

DEFAULT_CONFIG = {
    'dev': True,
    'file_types': ['ipynb', 'py'],
    'launcher_entry': LAUNCHER_ENTRY
}


def _get_config():
    """Load configuration from jupyter-panel-proxy.yml if present."""
    config_path = pathlib.Path('jupyter-panel-proxy.yml')
    config = dict(DEFAULT_CONFIG)
    if config_path.is_file():
        with open(config_path) as f:
            config.update(yaml.load(f.read(), Loader=yaml.BaseLoader))
    return config


def _search_apps(config):
    """Search for apps based on file types configured."""
    base_dir = pathlib.Path('./')
    example_dir = base_dir / 'examples'
    if example_dir.is_dir():
        base_path = example_dir
    else:
        base_path = base_dir
    apps = []
    for ft in config.get('file_types', []):
        apps += [str(app) for app in base_path.glob(f'**/*.{ft}')]
    return apps


def _discover_apps():
    """Discover apps according to configuration and exclusion patterns."""
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
    """Build the `panel serve` launch command based on configuration."""
    config = _discover_apps()

    command = [
        "panel", "serve",
        *config.get('apps'),
        "--allow-websocket-origin", "*",
        "--port", f"{port}",
        "--prefix", "{base_url}panel",
        "--disable-index-redirect"
    ]

    # Boolean flags
    for flag in ['autoreload', 'warm', 'admin', 'dev', 'reuse_sessions', 'liveness']:
        if config.get(flag):
            command.append(f'--{flag.replace("_", "-")}')

    # Numeric flags
    numeric_flags = {
        'num_procs': '--num-procs',
        'num_threads': '--num-threads',
        'keep_alive': '--keep-alive',
        'check_unused_sessions': '--check-unused-sessions',
        'unused_session_lifetime': '--unused-session-lifetime',
        'websocket_max_message_size': '--websocket-max-message-size',
        'stats_log_frequency': '--stats-log-frequency',
        'mem_log_frequency': '--mem-log-frequency',
        'session_token_expiration': '--session-token-expiration'
    }
    for key, arg in numeric_flags.items():
        if key in config:
            command += [arg, str(config[key])]

    # String flags
    string_flags = {
        'root_path': '--root-path',
        'cookie_path': '--cookie-path',
        'log_level': '--log-level',
        'liveness_endpoint': '--liveness-endpoint',
        'profiler': '--profiler',
        'index': '--index'
    }
    for key, arg in string_flags.items():
        if key in config:
            command += [arg, str(config[key])]

    # List flags
    list_flags = {
        'static_dirs': '--static-dirs',
        'oauth_guest_endpoints': '--oauth-guest-endpoints'
    }
    for key, arg in list_flags.items():
        if key in config:
            for val in config[key]:
                command += [arg, str(val)]

    # OAuth configuration
    if 'oauth_provider' in config:
        from cryptography.fernet import Fernet
        from bokeh.util.token import generate_secret_key
        command += ['--oauth-provider', config['oauth_provider']]

        encryption_key = config.get('oauth_encryption_key') or os.environ.get('OAUTH_ENCRYPTION_KEY')
        if not encryption_key:
            encryption_key = Fernet.generate_key()
        command += ['--oauth-encryption-key', encryption_key]

        cookie_secret = config.get('cookie_secret') or os.environ.get('PANEL_COOKIE_SECRET')
        if not cookie_secret:
            cookie_secret = generate_secret_key()
        command += ['--cookie-secret', cookie_secret]

    if 'oauth_key' in config:
        command += ['--oauth-key', config['oauth_key']]

    if 'oauth_secret' in config:
        command += ['--oauth-secret', config['oauth_secret']]

    if 'oauth_redirect_uri' in config:
        command += ['--oauth-redirect-uri', config['oauth_redirect_uri']]

    if 'oauth_jwt_user' in config:
        command += ['--oauth-jwt-user', config['oauth_jwt_user']]

    if 'oauth_extra_params' in config:
        command += ['--oauth-extra-params', repr(config['oauth_extra_params'])]

    if config.get('oauth_optional'):
        command.append('--oauth-optional')

    # Global loading spinner
    if config.get('global_loading_spinner'):
        command.append('--global-loading-spinner')

    return command


def setup_panel_server():
    """Entry point for Jupyter Server Proxy."""
    config = _get_config()
    spec = {
        'command': _launch_command,
        'absolute_url': True,
        'timeout': 360
    }
    if 'launcher_entry' in config:
        spec['launcher_entry'] = config['launcher_entry']
    return spec
