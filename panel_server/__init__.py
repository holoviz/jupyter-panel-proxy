from glob import glob

def setup_panel_server():
    return {
        'command': ["panel", "serve", *glob('./**/*.ipynb', recursive=True), "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}panel", "--autoreload"],
        'absolute_url': True,
        'timeout': 360,
    }
