"""Setuptools configuration for rpmvenv."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='rpmvenv',
    version='0.18.0',
    url='https://github.com/kevinconway/rpmvenv',
    description='RPM packager for Python virtualenv.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license='MIT',
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[
        'jinja2',
        'venvctrl',
        'argparse',
        'confpy',
        'ordereddict',
        'semver',
    ],
    entry_points={
        'console_scripts': [
            'rpmvenv = rpmvenv.cli:main',
        ],
        'rpmvenv.extensions': [
            'core = rpmvenv.extensions.core:Extension',
            'file_permissions = rpmvenv.extensions.files.permissions:Extension',
            'file_extras = rpmvenv.extensions.files.extras:Extension',
            'python_venv = rpmvenv.extensions.python.venv:Extension',
            'blocks = rpmvenv.extensions.blocks.generic:Extension',
        ]
    },
    package_data={
        "rpmvenv": ["templates/*"],
    },
)
