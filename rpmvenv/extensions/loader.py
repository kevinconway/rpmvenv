"""Tools for loading and validating extensions."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pkg_resources
import semver


class MissingDependency(Exception):

    """No dependency found."""


class InvalidDependency(Exception):

    """Found dependency but with the wrong version."""


def load_extensions(whitelist=()):
    """Get an iterable of extensions in order."""
    whitelist = tuple(('core',) + tuple(whitelist))
    unique_whitelist = tuple(set(whitelist))
    extensions = pkg_resources.iter_entry_points('rpmvenv.extensions')
    extensions = (
        extension for extension in extensions if extension.name in unique_whitelist
    )
    extensions = tuple(set(extensions))
    extensions = sorted(extensions, key=lambda ext: whitelist.index(ext.name))
    return tuple(extension.load() for extension in extensions)


def validate_extensions(extensions):
    """Process the extension dependencies."""
    ext_map = dict(
        (ext.name, ext) for ext in extensions
    )

    for ext in extensions:

        for dependency, versions in ext.requirements.items():

            ext_dependency = ext_map.get(dependency, None)
            if not ext_dependency:

                raise MissingDependency(
                    '{0} is required by {1} but is not loaded.'.format(
                        ext.name,
                        dependency,
                    )
                )

            for version in versions:

                if not semver.match(ext.version, version):

                    raise InvalidDependency(
                        '{0}-{1} required by {2} but found {0}-{3}.'.format(
                            dependency,
                            version,
                            ext.name,
                            ext.version,
                        )
                    )

    return extensions
