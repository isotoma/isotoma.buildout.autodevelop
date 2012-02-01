from setuptools import setup, find_packages

version = '0.0.14'

setup(
    name = "isotoma.buildout.autodevelop",
    version = version,
    description = "Buildout extension to automatically develop eggs found in specified directories.",
    url = "http://pypi.python.org/pypi/isotoma.buildout.autodevelop",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    classifiers = [
        "Framework :: Buildout",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "buildout extension log",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup.py']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
    },
    namespace_packages = ['isotoma', 'isotoma.buildout'],
    include_package_data = True,
    zip_safe = False,
    entry_points = {
        'zc.buildout.extension': ['ext = isotoma.buildout.autodevelop:load'],
        },
    install_requires = [
        'setuptools',
        'zc.buildout',
        ],
    )

