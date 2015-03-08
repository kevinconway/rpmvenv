"""Extensions which package files not typically in the buildroot."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import PatternOption

from .. import interface


cfg = Configuration(
    file_extras=Namespace(
        description='Add default file permissions to files in buildroot.',
        files=ListOption(
            description='Files to move as src:dest. Relative to the root.',
            option=PatternOption(pattern='.*:.*'),
            default=(),
        ),
    ),
)


class Extension(interface.Extension):

    """Extension which adds packaging of extra files."""

    name = 'file_extras'
    description = 'Package files not in the buildroot.'
    version = '1.0.0'
    requirements = {
        'file_permissions': ('>=1.0.0', '<2.0.0'),
    }

    @staticmethod
    def generate(config, spec):
        """Produce file block segments for setting permissions."""
        for file_ in config.file_extras.files:

            src, dest = file_.split(':')
            spec.blocks.install.append(
                'mkdir -p "%{{buildroot}}/%(dirname {0})"'.format(dest)
            )
            spec.blocks.install.append(
                'cp -R %{{SOURCE0}}/{0} %{{buildroot}}/{1}'.format(
                    src,
                    dest,
                )
            )
            spec.blocks.files.append('/{0}'.format(dest))
            spec.blocks.post.append(
                'chown -R '
                '%{{file_permissions_user}}:%{{file_permissions_group}} '
                '/{0}'.format(dest)
            )

        return spec
