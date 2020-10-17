"""Extension for packaging a Python virtualenv."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import StringOption
from confpy.api import BoolOption

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
        require_setup_py=BoolOption(
            description='Whether to build the rpm with the use of setup.py. '
                        'When false can be used to repackage a wheel',
            required=False,
            default=True,
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
        strip_binaries=BoolOption(
            description='Whether to strip native modules of debug information '
                        'that often contains the buildroot paths',
            required=False,
            default=True,
        ),
        use_pip_install=BoolOption(
            description='Whether to use pip install to install the package '
                        'in the venv',
            required=False,
            default=False,
        ),
        remove_pycache=BoolOption(
            description='Whether to remove compiled bytecode to reduce '
                        'package size.',
            required=False,
            default=False,
        ),
    ),
)


class Extension(interface.Extension):

    """Extension for packaging a Python virtualenv."""

    name = 'python_venv'
    description = 'Packaging extension for generating virtualenv.'
    version = '1.0.0'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Generate Python virtualenv content."""
        spec.macros['venv_cmd'] = '{0} {1}'.format(
            config.python_venv.cmd,
            ' '.join(
                config.python_venv.flags if config.python_venv.flags else ()
            ),
        )
        if config.python_venv.python:

            spec.macros['venv_cmd'] = '{0} --python={1}'.format(
                spec.macros['venv_cmd'],
                config.python_venv.python,
            )
        spec.macros['venv_name'] = config.python_venv.name
        spec.macros['venv_install_dir'] = '{0}/%{{venv_name}}'.format(
            config.python_venv.path,
        )
        spec.macros['venv_dir'] = '%{buildroot}/%{venv_install_dir}'
        spec.macros['venv_bin'] = '%{venv_dir}/bin'
        spec.macros['venv_python'] = '%{venv_bin}/python'
        spec.macros['venv_pip'] = (
            '%{{venv_python}} %{{venv_bin}}/pip install {0}'.format(
                ' '.join(
                    config.python_venv.pip_flags
                    if config.python_venv.pip_flags
                    else ()
                ),
            )
        )
        spec.macros['__prelink_undo_cmd'] = "%{nil}"

        spec.globals['__os_install_post'] = (
            "%(echo '%{__os_install_post}' | sed -e "
            "'s!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:"
            "]].*$!!g')"
        )

        spec.tags['AutoReq'] = 'No'
        spec.tags['AutoProv'] = 'No'

        spec.blocks.prep.append(
            'mkdir -p %{buildroot}/%{venv_install_dir}',
        )

        spec.blocks.files.append('/%{venv_install_dir}')

        spec.blocks.install.append('%{venv_cmd} %{venv_dir}')
        for requirement in config.python_venv.requirements:

            spec.blocks.install.extend((
                'cd %{SOURCE0}',
                '%{{venv_pip}} -r {0}'.format(requirement),
                'cd -',
            ))

        if config.python_venv.require_setup_py:
            spec.blocks.install.append('cd %{SOURCE0}')

            if config.python_venv.use_pip_install:
                spec.blocks.install.append('%{venv_pip} .')
            else:
                spec.blocks.install.append('%{venv_python} setup.py install')

            spec.blocks.install.append('cd -')

        if config.python_venv.remove_pycache:
            spec.blocks.install.append(
                r'find %{venv_dir} -type d -name "__pycache__" -print0 | '
                r'xargs -0 rm -rf'
            )

        spec.blocks.install.extend((
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

        if config.python_venv.strip_binaries:
            spec.blocks.install.extend((
                '# Strip native modules as they contain buildroot paths in'
                'their debug information',
                'find %{venv_dir}/lib -type f -name "*.so" | xargs -r strip',
            ))
        else:
            spec.macros["debug_package"] = "debug_package %{nil}"
            spec.macros["__strip"] = "/bin/true"
            # Several RPM bundles and dev packages, like redhat-rpm-config and
            # rpm-devel inject macros into every RPM spec by modifying the
            # global RPM configuration. This disables the known macros from
            # those packages that inject an additional binary strip step.
            # See https://github.com/kevinconway/rpmvenv/pull/93 for details.

        return spec
