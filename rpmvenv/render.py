"""Functions for rendering a SPEC file."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


REQUIRED_RC_VALUES = (
    'pkg_name',
    'pkg_version',
)


def macros(template, **kwargs):
    """Render a series of define statements with parameters.

    Args:
        template: A jinja2 template to render with macro values.

    Keyword Args:
        pkg_name: The name of the direcotory containing the package content.
            (Required)
        pkg_version: The version number to assign the RPM. (Required)
        pkg_rpm_name: The name of the RPM package. The default is to use
            the pkg_name macro.
        pkg_release: The number of times this version has been released.
            The default is 1.
        pkg_group: The RPM group in which the package belongs. The default is
            Applications/System.
        pkg_summary: A short, one line summary of the package contents. The
            default is a copy of the package name.
        pkg_license: The license under which the package code is distributed.
            The default is No License.
        pkg_url: A URL to the package source contents. The default is a copy of
            the package name.
        pkg_source: A URL or path to the project source code. The last element
            in the path must be the pkg_name value. The default value is a copy
            of the package name.
        pkg_install_dir: The path, relative to the root directory, in which the
            package content will be installed on a host. The default value is
            /user/share/python.
        pkg_user: The system user to create which will have ownership of the
            installed files. The default is root.
        pkg_user_group: The system group to create which will have ownership of
            the installed files. The default is root.

    Note:
        The documented keyword arguments are used to provide the core
        functionality. Extra keyword arguments may be given in order to inject
        other, custom, macros into the SPEC file if desired.
    """
    macro_values = kwargs.copy()
    for required_value in REQUIRED_RC_VALUES:

        if required_value not in macro_values:

            raise ValueError(
                'Missing required macro value {0}.'.format(required_value)
            )

    macro_values.setdefault('pkg_rpm_name', macro_values['pkg_name'])
    macro_values.setdefault('pkg_release', 1)
    macro_values.setdefault('pkg_summary', macro_values['pkg_name'])
    macro_values.setdefault('pkg_group', 'Applications/System')
    macro_values.setdefault('pkg_license', 'No License')
    macro_values.setdefault('pkg_url', macro_values['pkg_name'])
    macro_values.setdefault('pkg_source', macro_values['pkg_name'])
    macro_values.setdefault('pkg_install_dir', 'usr/share/python')
    macro_values.setdefault('pkg_user', 'root')
    macro_values.setdefault('pkg_user_group', 'root')

    return template.render(macros=macro_values.items())


def spec(
        template,
        description='%{pkg_name}',
        python=None,
        venv_options=(),
        pip_options=(),
        requirements=('requirements.txt',),
        extra_files=(),
        posts=(),
        postuns=(),
):
    """Render a SPEC file with parameters.

    Args:
        template: The jinja2 template to render.
        description (str): An extended, multi-line description of the package.
            This defaults to the %{pkg_name} macro.
        python (str): The Python interpreter to use when creating the
            virtualenv. The default option is to use the default Python
            interpreter.
        venv_options (iter of str): An iterable of flags to use while creating
            the virtualenv.
        requirements (iter of str): An iterable of file paths relative to the
            source root which identify requirements files to install before the
            source package itself. By default the standard requirements.txt
            will be installed. Replace with an empty iterable to install no
            requirements files. If a custom list is passed it will overwrite
            the default which means requirements.txt must be in the custom list
            for it to be installed as well.
        extra_files (iter of tuple(str, str)): An iterable of two tuples where
            the first element is a path relative to the source root which
            should be installed on a host system. The second element is a path
            relative to the host system root where the file should be
            installed. Ex: (('bin/init.sh', 'etc/init.d/myproject'))
        posts (iter of str): An iterable of commands to run during the post
            install phase.
        postuns (iter of str): An iterable of commands to run during the postun
            install phase.
    """
    venv_options = list(venv_options)
    venv_options.append('--always-copy')
    if python:

        venv_options.append('--python={0}'.format(python))

    return template.render(
        description=description,
        venv_options=venv_options,
        pip_options=pip_options,
        requirements=requirements,
        extra_files=extra_files,
        posts=posts,
        postuns=postuns,
    )
