import param

from setuptools import find_packages, setup


extras_require = {
    'build': ['param >=1.7.0', 'setuptools'],
    'tests': [
        'flake8',
        'twine',
        'rfc3986',
        'keyring'
    ],
}

setup_args = dict(
    name="jupyter-panel-proxy",
    description='Jupyter Server Proxy for Panel applications',
    version=param.version.get_setup_version(
        __file__,
        "panel_server",
        archive_commit="$Format:%h$",
    ),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Julia Signell",
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
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires=">=3.6",
    install_requires=['jupyter-server-proxy', 'panel >=0.11'],
    extras_require=extras_require,
    packages=find_packages(),
    entry_points={
        'jupyter_serverproxy_servers': [
            'panel = panel_server:setup_panel_server',
        ]
    },
)

if __name__ == '__main__':
    setup(**setup_args)
