"""Command line functionality."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys

import confpy.api
import ordereddict
import pkg_resources
import shutil

from . import rpmbuild
from . import template


confpy.api.Configuration(
    extensions=confpy.api.Namespace(
        enabled=confpy.api.ListOption(
            description='The enabled extensions for the RPM build.',
            option=confpy.api.StringOption(),
            default=(),
        ),
    ),
)


def render_spec(config):
    """Render a spec file from a config mapping."""
    spectemplate = template.get('rpm.spec')
    return spectemplate.render(**config)


def render_defines(config):
    """Render the cli options for macro definitions."""
    macrotemplate = template.get('macros')
    return macrotemplate.render(**config)


def build_rpm(top, specfile, defines, source_dir, source_name):
    """Generate an RPM."""
    specfile = rpmbuild.write_spec(top, specfile)
    rpmbuild.copy_source(top, source_dir, name=source_name)
    pkg = rpmbuild.build(specfile=specfile, defines=defines, top=top)
    shutil.move(pkg, './')
    return os.path.join('./', os.path.basename(pkg))


def load_configuration_file(path):
    """Load a configuration file from the given path."""
    cfg = confpy.api.parse_options(
        (path,),
        env_prefix='RPMVENV',
        strict=False,
    )
    extensions = cfg.extensions.enabled
    extensions = load_extensions(whitelist=tuple(extensions))
    return confpy.api.parse_options(
        (path,),
        env_prefix='RPMVENV',
        strict=True,
    )


def load_extensions(whitelist=()):
    """Get an iterable of extensions in order."""
    whitelist = tuple(set(('core',) + tuple(whitelist)))
    extensions = pkg_resources.iter_entry_points('rpmvenv.extensions')
    extensions = (
        extension for extension in extensions if extension.name in whitelist
    )
    extensions = tuple(set(extensions))
    extensions = sorted(extensions, key=lambda ext: whitelist.index(ext.name))
    return tuple(
        (extension.name, extension.load()) for extension in extensions
    )


def build_config(cfg, extensions, base=None):
    """Generate a config mapping from a set of extensions."""
    payload = base or {}
    for name, ext in extensions:

        values = ext.generate(getattr(cfg, name))
        payload.setdefault(
            'macros',
            [],
        ).extend(values.setdefault('macros', ()))
        payload.setdefault(
            'defines',
            [],
        ).extend(values.setdefault('defines', ()))
        payload.setdefault(
            'globals',
            [],
        ).extend(values.setdefault('globals', ()))
        payload.setdefault(
            'tags',
            [],
        ).extend(values.setdefault('tags', ()))

        for block_name, block_lines in values.setdefault('blocks', ()):

            payload.setdefault('blocks', {}).setdefault(block_name, []).extend(
                block_lines,
            )

    for key, value in payload.items():

        payload[key] = ordereddict.OrderedDict(value)

    return payload


def build_from_mapping(mapping, source, name):
    """Build an RPM from a configuration mapping."""
    specfile = render_spec(mapping)
    defines = render_defines(mapping)
    top = rpmbuild.topdir()
    rpm_path = build_rpm(top, specfile, defines, source, name)
    shutil.rmtree(top)
    return rpm_path


def build_from_path(path):
    """Build an RPM from a configuration file."""
    cfg = load_configuration_file(path)
    extensions = load_extensions(whitelist=cfg.extensions.enabled)
    mapping = build_config(cfg, extensions)
    return build_from_mapping(mapping, os.path.dirname(path), cfg.core.name)


def main():
    """Build an RPM."""
    parser = argparse.ArgumentParser(description="Generate an RPM.")
    parser.add_argument(
        'config',
        help='The path to a configuration file.',
    )
    args, _ = parser.parse_known_args()
    try:

        pth = os.path.abspath(args.config)
        rpm_path = build_from_path(pth)

    except rpmbuild.RpmProcessError as exc:

        sys.stderr.write('There was an error generated the RPM.{0}'.format(
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

    sys.stdout.write('RPM generated at {0}{1}.'.format(rpm_path, os.linesep))
    sys.exit(0)

if __name__ == '__main__':

    main()
