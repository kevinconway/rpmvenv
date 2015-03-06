"""Extensions which set file permissions for all packaged files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import Namespace
from confpy.api import StringOption

from .. import interface


cfg = Configuration(
    file_permissions=Namespace(
        description='Add default file permissions to files in buildroot.',
        user=StringOption(
            description='The owner user.',
            required=True,
        ),
        group=StringOption(
            description='The owner group.',
            required=True,
        ),
    ),
)


class Extension(interface.Extension):

    """Extension which adds default file permissions."""

    name = 'file_permissions'
    description = 'Set default file permissions to a user and group.'

    @staticmethod
    def generate(namespace):
        """Produce file block segments for setting permissions."""
        return {
            "macros": (),
            "defines": (),
            "globals": (),
            "tags": (),
            "blocks": (
                ('files', (
                    '%defattr(-,{0},{1},-)'.format(
                        namespace.user,
                        namespace.group,
                    ),
                )),
            ),
        }
