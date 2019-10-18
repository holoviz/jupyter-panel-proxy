from glob import glob

def setup_panel_server():
    return {
        'command': ["panel", "serve", *glob('*.ipynb'), "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}panel"],
        'absolute_url': True,
        'timeout': 360,
    }
