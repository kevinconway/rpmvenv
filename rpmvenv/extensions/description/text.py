"""Description provider which uses text value."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import Namespace
from confpy.api import StringOption

from .. import interface


cfg = Configuration(
    description_text=Namespace(
        description='Simple text RPM description provider.',
        text=StringOption(
            description='The literal description to set within the RPM',
            required=True,
        ),
    ),
)


class Extension(interface.Extension):

    """Simple text provider for RPM descriptions."""

    name = 'description_text'
    description = 'A simple text description provider.'

    @staticmethod
    def generate(namespace):
        """Set the description from a config value."""
        return {
            "macros": (),
            "defines": (),
            "globals": (),
            "tags": (),
            "blocks": (
                (
                    'description', (
                        namespace.text,
                    ),
                ),
            ),
        }
