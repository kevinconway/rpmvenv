"""Standard interface for all extensions.

All extensions must expose, as an entry_point under rpmvenv.extensions, a
Python object. The object must expose 'name', 'description', 'version',
'requirements', and 'generate' attributes. Optionally, the module containing
the entry_point target may define a confpy Configuration object with one, or
more, Namespaces.

The 'name' attribute must be a string value which identifies the extension.
It should match the name chosen within the entry_point.

The 'description' attribute must be a string, optionally with multiple lines,
which describes the features provided by the extension.

The 'version' attribute must be a valid semantic versioning string which
identifies the current state of the extension.

The 'requirements' attribute must be mapping. Each key in the mapping must
identify another extension by name which must be loaded before the current
extension. The value of each key must be an iterable of version specifiers
such as '>=1.0' or '==2.3.4'. Each entry in the iterable will be used to
validate the requirement version.

The 'generate' attribute must be a Python callable, such as a function, which
consumes as input an initialized confpy Configuration object as the first
argument and a partially initialized Spec object as the second argument.

The 'generate' callable must return a Spec object.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Extension(object):

    """An example extension."""

    name = 'example'
    description = "An example extension."
    version = '0.1'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Generate the mapping described in the module docstring."""
        raise NotImplementedError()
