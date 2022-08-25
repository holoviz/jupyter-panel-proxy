# Jupyter Server Proxy for Panel

When jupyter-panel-proxy is installed and you launch a Jupyter server (Notebook, JupyterLab or JupyterHub), a Panel server will be launched when you visit the `/panel` endpoint of the server. This will show an index of all applications being served, to launch a particular application visit the corresponding endpoint `/panel/<name_of_file>`.

## Installation

The `jupyter-panel-proxy` is available from `pip`:

    pip install jupyter-panel-proxy
    
and conda:

    conda install -c pyviz jupyter-panel-proxy

## Configuration

The jupyter-panel-proxy provides the ability to configure the proxy server by declaring a `jupyter-panel-proxy.yml` in the directory the Jupyter server is being launched from. The `yaml` file may declare the following keys: 

- `apps` (`list`): A list of applications or glob patterns to serve
- `launcher_entry` (`dict`): A [jupyter-server-proxy launcher entry specification](https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html#launcher-entry)
- `file_types` (`list(str)`): A list of file types to serve if no explicit apps list is provided
- `exclude_patterns` (`list(str)`): A list of glob/(fnmatch) patterns to exclude specific applications
- `index` (`str`): The path to a Bokeh index template
- `autoreload` (`bool`): Whether to automatically reload user sessions when the application or any of its imports change.
- `admin` (`bool`): Whether to load panel's admin module.
- `static_dirs` (`list`): A list of dicts mapping from server route to the static directory to be served 
- `warm` (`bool`): Whether to execute scripts on startup to warm up the server.
- `num_procs` (`int`): Number of worker processes for an app. Using 0 will autodetect number of cores (defaults to 1)
- `oauth_provider` (`str`): The OAuth2 provider to use.
- `oauth-key` (`str`): The OAuth2 key to use
- `oauth-secret` (`str`): The OAuth2 secret to use
- `oauth-redirect-uri` (`str`): The OAuth2 redirect URI
- `oauth_extra_params` (`dict`): Additional parameters to the OAuth provider.
- `oauth_jwt_user` (`str`): The key in the ID JWT token to consider the user.
