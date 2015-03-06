"""Standard interface for all extensions.

All extensions must expose, as an entry_point under rpmvenv.extensions, a
Python object. The object must expose 'name', 'description', and 'generate'
attributes. Optionally, the module containing the entry_point target may
define a confpy Config object with a single Namespace. The name of the
Namespace must match the 'name' attribute of the extension which must, in turn,
match the entry_point target name.

The 'name' attribute must be a string value which identifies the extension.
It should match the name chosen within the entry_point.

The 'description' attribute must be a string, optionally with multiple lines,
which describes the features provided by the extension.

The 'generate' attribute must be a Python callable, such as a function, which
consumes, as input, the Namespace object from confpy which is keyed by the same
name as the entry_point name. For example, if the following entry_point is
given::

    "entry_points": {
        "rpmvenv.extensions": [
            "cool_feature = somepackage.somemodule:the_extension",
        ]
    }

Then 'the_extension.generate' will be given a namespace defined in the config
file as 'cool_feature'. If no namespace is found in the config file 'None' will
be given instead.

The 'generate' callable must return a mapping in the following format:

{
    "macros": (
        ("macro_name", "macro_value"),
    ),
    "defines": (
        ("define_name", "define_value"),
    ),
    "globals": (
        ("global_name", "global_value"),
    ),
    "tags": (
        ("tag_name", "tag_value")
    ),
    "blocks": (
        (
            "block_name", ("block_line",),
        ),
    ),
}

All values in the mapping must be iterables of key value pairs. With the
exception of the "section" key all key value pairs must be string values.
The value of each entry in the "section" key must be an iterable strings.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Extension(object):

    """An example extension."""

    name = 'example'
    description = "An example extension."

    @staticmethod
    def generate(namespace):
        """Generate the mapping described in the module docstring."""
        raise NotImplementedError()
