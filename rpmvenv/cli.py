"""Command line functionality."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import shutil
import subprocess
import sys

import confpy.api

from .extensions import loader as extensions_loader
from . import rpmbuild
from . import spec


confpy.api.Configuration(
    extensions=confpy.api.Namespace(
        enabled=confpy.api.ListOption(
            description='The enabled extensions for the RPM build.',
            option=confpy.api.StringOption(),
            default=(),
        ),
    ),
)


def parse_args(argv):
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description='Generate an RPM.')
    parser.add_argument(
        'config',
        help='The path to a configuration file.',
    )
    parser.add_argument(
        '--source',
        help='Path to package source. Default is config parent directory.',
        default=None,
    )
    parser.add_argument(
        '--destination',
        help='Output path for final RPM. Default is current directory.',
        default='./',
    )
    parser.add_argument(
        '--spec',
        help='Print the SPEC file without generating an RPM with it.',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--verbose',
        help='Enable real-time streaming output of rpmbuild.',
        default=False,
        action='store_true',
    )
    args, _ = parser.parse_known_args(argv)
    args = vars(args)
    args['config'] = os.path.abspath(args['config'])
    args['source'] = (
        os.path.abspath(args['source'])
        if args['source']
        else os.path.dirname(args['config'])
    )
    return args


def generate_rpm(source, destination, specfile, verbose=False):
    """Generate an RPM from the given arguments mapping."""
    top = rpmbuild.topdir()
    rpmbuild.copy_source(top, source)
    specfile = rpmbuild.write_spec(top, specfile)
    pkg = rpmbuild.build(specfile=specfile, top=top, verbose=verbose)
    shutil.move(pkg, destination)
    return os.path.join(destination, os.path.basename(pkg))


def generate_spec(config, extensions):
    """Generate a SPEC file from the given arguments mapping."""
    specfile = spec.Spec()
    for ext in extensions:

        specfile = ext.generate(config, specfile)

        if not specfile:

            sys.stderr.write(
                'The {0} extension did not return a valid '
                'Spec object.{1}'.format(ext.name, os.linesep)
            )
            sys.exit(1)

    return str(specfile)


def main(argv=sys.argv[1:]):
    """Build an RPM."""
    args = parse_args(argv)
    config = confpy.api.parse_options(
        files=(args['config'],),
        env_prefix='RPMVENV',
        strict=False,
    )
    whitelist = tuple(config.extensions.enabled)
    extensions = extensions_loader.load_extensions(whitelist=whitelist)
    config = confpy.api.parse_options(
        files=(args['config'],),
        env_prefix='RPMVENV',
        strict=True,
    )
    config.core.source = args['source']

    try:

        extensions_loader.validate_extensions(extensions)

    except (
            extensions_loader.MissingDependency,
            extensions_loader.InvalidDependency,
    ) as exc:

        sys.stderr.write('{0}{1}'.format(str(exc), os.linesep))
        sys.exit(1)

    specfile = generate_spec(config, extensions)

    if args['spec']:

        sys.stdout.write('{0}{1}'.format(specfile, os.linesep))
        sys.exit(0)

    try:

        rpm_path = generate_rpm(
            args['source'],
            args['destination'],
            specfile,
            args['verbose'],
        )

    except rpmbuild.RpmProcessError as exc:

        sys.stderr.write('There was an error generating the RPM.{0}'.format(
            os.linesep,
        ))
        sys.stderr.write('The exit code was: {0}.{1}'.format(
            exc.returncode,
            os.linesep,
        ))
        sys.stderr.write('The rpmbuild command was: {0}.{1}'.format(
            exc.cmd,
            os.linesep,
        ))
        sys.stderr.write('The stderr was: {0}.{1}'.format(
            exc.stderr,
            os.linesep,
        ))
        sys.stderr.write('The stdout was: {0}.{1}'.format(
            exc.stdout,
            os.linesep,
        ))
        sys.exit(1)

    except subprocess.CalledProcessError as exc:

        sys.stderr.write('There was an error generating the RPM.{0}'.format(
            os.linesep,
        ))
        sys.stderr.write('The exit code was: {0}.{1}'.format(
            exc.returncode,
            os.linesep,
        ))
        sys.stderr.write('The rpmbuild command was: {0}.{1}'.format(
            exc.cmd,
            os.linesep,
        ))
        sys.exit(1)

    sys.stdout.write('RPM generated at {0}{1}.'.format(rpm_path, os.linesep))
    sys.exit(0)


if __name__ == '__main__':

    main()
