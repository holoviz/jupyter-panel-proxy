import os
import setuptools


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    import json
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from param import version
    except:
        version = None
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']

extras_require = {
    'build': ['param >=1.7.0', 'setuptools']
}

setuptools.setup(
    name="jupyter-panel-proxy",
    packages=setuptools.find_packages(),
    description='Jupyter Server Proxy for Panel applications',
    long_description=open('README.md').read() if os.path.isfile('README.md') else 'Consult README.md',
    long_description_content_type="text/markdown",
    author= "PyViz developers",
    author_email= "",
    maintainer= "PyViz",
    maintainer_email= "developers@pyviz.org",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    entry_points={
        'jupyter_serverproxy_servers': [
            'panel = panel_server:setup_panel_server',
        ]
    },
    install_requires=['jupyter-server-proxy', 'panel'],
    extras_require=extras_require,
)
