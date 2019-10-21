import os
import setuptools


########## autover ##########

def embed_version(basepath, ref='v0.2.2'):
    """
    Autover is purely a build time dependency in all cases (conda and
    pip) except for when you use pip's remote git support [git+url] as
    1) you need a dynamically changing version and 2) the environment
    starts off clean with zero dependencies installed.
    This function acts as a fallback to make Version available until
    PEP518 is commonly supported by pip to express build dependencies.
    """
    import io, zipfile, importlib
    try:    from urllib.request import urlopen
    except: from urllib import urlopen
    try:
        url = 'https://github.com/ioam/autover/archive/{ref}.zip'
        response = urlopen(url.format(ref=ref))
        zf = zipfile.ZipFile(io.BytesIO(response.read()))
        ref = ref[1:] if ref.startswith('v') else ref
        embed_version = zf.read('autover-{ref}/autover/version.py'.format(ref=ref))
        with open(os.path.join(basepath, 'version.py'), 'wb') as f:
            f.write(embed_version)
        return importlib.import_module("version")
    except:
        return None

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
        version = embed_version(basepath)
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']


extras_require = {
    'build': ['param >=1.7.0', 'setuptools'],
    'tests': ['flake8'],
}

setuptools.setup(
    name="jupyter-panel-proxy",
    packages=setuptools.find_packages(),
    description='Jupyter Server Proxy for Panel applications',
    version=get_setup_version('panel_server'),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author= "Julia Signell",
    author_email= "developers@pyviz.org",
    maintainer= "PyViz developers",
    maintainer_email= "developers@pyviz.org",
    url="https://github.com/pyviz/jupyter-panel-proxy",
    project_urls = {
        "Bug Tracker": "http://github.com/pyviz/jupyter-panel-proxy/issues",
        "Documentation": "https://github.com/pyviz/jupyter-panel-proxy/blob/master/README.md",
        "Source Code": "https://github.com/pyviz/jupyter-panel-proxy",
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
    install_requires=['jupyter-server-proxy', 'panel'],
    extras_require=extras_require,
)
