"""Setuptools configuration for rpmvenv."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='rpmvenv',
    version='0.4.0',
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
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'rpmvenv = rpmvenv.cmd:main',
        ],
    },
    package_data={
        "rpmvenv": ["templates/*"],
    },
)
