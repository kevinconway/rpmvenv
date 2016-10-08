"""Extensions which set file permissions for all packaged files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import BoolOption
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
        create_user=BoolOption(
            description='Create the user if it does not exist.',
            default=False,
        ),
        group=StringOption(
            description='The owner group.',
            required=True,
        ),
        create_group=BoolOption(
            description='Create the group if it does not exist.',
            default=False
        ),
    ),
)


class Extension(interface.Extension):

    """Extension which adds default file permissions."""

    name = 'file_permissions'
    description = 'Set default file permissions to a user and group.'
    version = '1.0.0'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Produce file block segments for setting permissions."""
        spec.macros['file_permissions_user'] = config.file_permissions.user
        spec.macros['file_permissions_group'] = config.file_permissions.group
        spec.blocks.files.insert(
            0,
            '%defattr(-,%{file_permissions_user},%{file_permissions_group},-)'
        )
        if config.file_permissions.create_user:

            spec.blocks.pre.append(
                'id -u %{file_permissions_user} &>/dev/null || '
                'useradd %{file_permissions_user}'
            )

        if config.file_permissions.create_group:

            spec.blocks.pre.append(
                'id -g %{file_permissions_group} &>/dev/null || '
                'groupadd %{file_permissions_group}'
            )

        return spec
