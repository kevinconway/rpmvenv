"""Extension for packaging a Python virtualenv."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import StringOption

from .. import interface


cfg = Configuration(
    python_venv=Namespace(
        description='Generate RPMs from Python virtualenv.',
        cmd=StringOption(
            description='The executable to use for creating a venv.',
            default='virtualenv',
        ),
        flags=ListOption(
            description='Flags to pass to the venv during creation.',
            option=StringOption(),
            default=('--always-copy',),
        ),
        name=StringOption(
            description='The name of the installed venv.',
            required=True,
        ),
        path=StringOption(
            description='The path in which to install the venv.',
            default='/usr/share/python',
        ),
        python=StringOption(
            description='The python executable to use in the venv.',
            required=False,
        ),
        requirements=ListOption(
            description='Names of requirements files to install in the venv.',
            option=StringOption(),
            default=('requirements.txt',)
        ),
        pip_flags=ListOption(
            description='Flags to pass to pip during pip install calls.',
            option=StringOption(),
            default=(),
        ),
    ),
)


class Extension(interface.Extension):

    """Extension for packaging a Python virtualenv."""

    name = 'python_venv'
    description = 'Packaging extension for generating virtualenv.'

    @staticmethod
    def generate(namespace):
        """Generate Python virtualenv blocks and macros."""
        venv_pip = '%{{venv_python}} %{{venv_bin}}/pip install {0}'.format(
            ' '.join(namespace.pip_flags if namespace.pip_flags else ()),
        )
        venv_cmd = '{0} {1}'.format(
            namespace.cmd,
            ' '.join(namespace.flags if namespace.flags else ()),
        )
        if namespace.python:

            venv_cmd = '{0} --python={1}'.format(venv_cmd, namespace.python)

        install_steps = [
            '%{venv_cmd} %{venv_dir}',
        ]
        for requirement in namespace.requirements:

            install_steps.append(
                '%{{venv_pip}} -r %{{SOURCE0}}/{0}'.format(
                    requirement,
                )
            )

        install_steps.extend((
            'pushd %{SOURCE0}',
            '%{venv_python} setup.py install',
            'popd',
            '# RECORD files are used by wheels for checksum. They contain path'
            ' names which',
            '# match the buildroot and must be removed or the package will '
            'fail to build.',
            'find %{buildroot} -name "RECORD" -exec rm -rf {} \\;',
            '# Change the virtualenv path to the target installation '
            'direcotry.',
            'venvctrl-relocate --source=%{venv_dir}'
            ' --destination=/%{venv_install_dir}',

        ))

        return {
            "macros": (
                ('venv_cmd', venv_cmd),
                ('venv_name', namespace.name),
                ('venv_install_dir', '{0}/%{{venv_name}}'.format(
                    namespace.path,
                )),
                ('venv_dir', '%{buildroot}/%{venv_install_dir}'),
                ('venv_bin', '%{venv_dir}/bin'),
                ('venv_python', '%{venv_bin}/python'),
                ('venv_pip', venv_pip),
            ),
            "defines": (),
            "globals": (
                (
                    "__os_install_post",
                    "%(echo '%{__os_install_post}' | sed -e "
                    "'s!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:"
                    "]].*$!!g')",
                ),
            ),
            "tags": (
                ('AutoReq', 'No'),
                ('AutoProv', 'No'),
            ),
            "blocks": (
                ('prep', (
                    'mkdir -p %{buildroot}/%{venv_install_dir}',
                )),
                ('install', install_steps),
                ('files', (
                    '/%{venv_install_dir}',
                )),
            ),
        }
