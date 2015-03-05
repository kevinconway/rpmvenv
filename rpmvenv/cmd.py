"""Command line functionality."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import shutil
import sys

import yaml

from . import render
from . import rpmbuild
from . import template


def build(source, config):
    """Generate an RPM from a config file mapping.

    Args:
        source: The path to the package source.
        config (mapping): A mapping which represents a configuration file.

    Valid Keys:

        -   name => The package name.

        -   version => The package version.

        -   spec => Mapping of spec values.

            -   description => Long form description of the package.

            -   python => Python interpreter to use in virtualenv.

            -   venv_options => Iterable of virtualenv flags to use.

            -   extra_files => Iterable of two-tuples where the first element
                    is the path of the source file relative to the source root
                    and the second is the path of the installed file relative
                    to the system root.

            -   post => Iterable of post-install commands to run.

            -   postun => Iterable post-uninstall commands to run.

        -   macros => RPM macro definitions.

            -   pkg_name => The name of the RPM package.

            -   pkg_version => The version number to assign the RPM.

            -   pkg_release => The number of times this version has been
                    released. The default is 1.

            -   pkg_group => The RPM group in which the package belongs. The
                    default is Applications/System.

            -   pkg_summary => A short, one line summary of the package
                    contents. The default is a copy of the package name.

            -   pkg_license => The license under which the package code is
                    distributed. The default is No License.

            -   pkg_url => A URL to the package source contents. The default is
                    a copy of the package name.

            -   pkg_source => A URL or path to the project source code. The
                    last element in the path must be the pkg_name value. The
                    default value is a copy of the package name.

            -   pkg_install_dir => The path, relative to the root directory, in
                    which the package content will be installed on a host. The
                    default value is /user/share/python.

            -   pkg_user => The system user to create which will have ownership
                    of the installed files. The default is root.

            -   pkg_user_group => The system group to create which will have
                    ownership of the installed files. The default is root.
    """
    source = os.path.abspath(source)

    macrostemplate = template.get('macros')
    spectemplate = template.get('rpm.spec')

    macros = config.get('macros', {})
    defines = render.macros(macrostemplate, **macros)

    spec = config.get('spec', {})
    specfile = render.spec(spectemplate, **spec)

    top = rpmbuild.topdir()
    specfile = rpmbuild.write_spec(top, specfile)
    rpmbuild.copy_source(top, source)
    pkg = rpmbuild.build(specfile=specfile, defines=defines, top=top)
    shutil.move(pkg, config.get('output', './'))


def main():
    """Generate an RPM from a Python project."""
    parser = argparse.ArgumentParser(description='Generate an RPM.')
    parser.add_argument(
        '--source',
        help='The path to your Python source.',
        default='.',
    )
    parser.add_argument(
        '--version',
        help='The version of your Python package.',
    )
    parser.add_argument(
        '--python',
        help='The Python interpreter to use in the virtualenv.',
    )
    parser.add_argument(
        '--venv-option',
        dest='venv_options',
        help='Extra flags to pass to virtualenv.',
        action='append',
    )
    parser.add_argument(
        '--requirement',
        dest='requirements',
        help='Requirements files to install. (relative to source root)',
        action='append',
    )
    parser.add_argument(
        '--no-requirements',
        help='Disable installation of requirements.txt files.',
        action='store_true',
        default=False,
    )
    args = parser.parse_args()

    config = {}
    source = os.path.abspath(args.source)
    name = os.path.basename(source)
    path = os.path.abspath(source)
    if source.endswith('.yml') or source.endswith('.json'):

        path = os.path.dirname(source)
        name = os.path.basename(path)
        with open(source, 'r') as config_files:

            config = yaml.load(config_files.read())

    elif 'setup.py' not in os.listdir(source):

        raise ValueError('The given source is not a valid Python package.')

    if args.version:

        config['version'] = args.version

    if not config.get('version', None):

        raise ValueError('A package version must be given.')

    if args.python:

        config.setdefault('spec', {})['python'] = args.python

    if args.venv_options:

        config.setdefault('spec', {})['venv_options'] = args.venv_options

    if args.requirements:

        config.setdefault('spec', {})['requirements'] = args.requirements

    if (
            args.no_requirements or not
            os.path.exists(os.path.join(path, 'requirements.txt'))
    ):

        config.setdefault('spec', {})['requirements'] = ()

    config.setdefault('name', name)
    config.setdefault('macros', {})['pkg_name'] = config.get('name')
    config['macros']['pkg_version'] = config.get('version')

    try:

        return build(source=path, config=config)

    except rpmbuild.RpmProcessError as exc:

        sys.stderr.write('There was an error building the RPM.{0}'.format(
            os.linesep,
        ))

        sys.stderr.write('Exit code: {0}{1}'.format(
            exc.returncode,
            os.linesep,
        ))

        sys.stderr.write('Command: {0}{1}'.format(
            exc.cmd,
            os.linesep,
        ))

        sys.stderr.write('Stderr: {0}{1}'.format(
            exc.stderr,
            os.linesep,
        ))

        sys.stderr.write('Stdout: {0}{1}'.format(
            exc.stdout,
            os.linesep,
        ))
        sys.exit(1)


if __name__ == '__main__':

    main()
