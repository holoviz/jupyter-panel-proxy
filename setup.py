import os

import param

import setuptools


extras_require = {
    'build': ['param >=1.7.0', 'setuptools'],
    'tests': ['flake8'],
}

setuptools.setup(
    name="jupyter-panel-proxy",
    packages=setuptools.find_packages(),
    description='Jupyter Server Proxy for Panel applications',
    version=param.version.get_setup_version(
        __file__,
        "panel_server",
        archive_commit="$Format:%h$",
    ),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author= "Julia Signell",
    author_email= "developers@holoviz.org",
    maintainer= "HoloViz developers",
    maintainer_email= "developers@pyviz.org",
    url="https://github.com/holoviz/jupyter-panel-proxy",
    project_urls = {
        "Bug Tracker": "http://github.com/holoviz/jupyter-panel-proxy/issues",
        "Documentation": "https://github.com/holoviz/jupyter-panel-proxy/blob/master/README.md",
        "Source Code": "https://github.com/holoviz/jupyter-panel-proxy",
    },
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    entry_points={
        'jupyter_serverproxy_servers': [
            'panel = panel_server:setup_panel_server',
        ]
    },
     classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"],
    python_requires=">=2.7",
    install_requires=['jupyter-server-proxy', 'panel >=2.3'],
    extras_require=extras_require,
)
