"""Extension which packages files not typically in the buildroot."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace

from .option import FileOption
from .. import interface


cfg = Configuration(
    file_extras=Namespace(
        description='Package files not in the Python package.',
        files=ListOption(
            description='Extra files to include. Paths are relative to'
                        'buildroot.',
            option=FileOption(),
            default=(),
        ),
    ),
)


class Extension(interface.Extension):

    """Extension which adds packaging of extra files."""

    name = 'file_extras'
    description = 'Package files not in the buildroot.'
    version = '1.1.0'
    requirements = {
        'file_permissions': ('>=1.0.0', '<2.0.0'),
    }

    @staticmethod
    def generate(config, spec):
        """Produce file block segments for packaging files."""
        for file_ in config.file_extras.files:

            if file_.file_type is not None:
                if file_.file_type_option is not None:
                    # file with a modifier (e.g. config) including an option
                    # (e.g. noreplace)
                    file_directive = '%{1}({2}) /{0}'.format(
                        file_.dest,
                        file_.file_type,
                        file_.file_type_option
                    )
                else:
                    # file with a modifier (e.g. doc) but no additional option
                    file_directive = '%{1} /{0}'.format(file_.dest,
                                                        file_.file_type)
            else:
                # simple file without an extra modifiers
                file_directive = '/{0}'.format(file_.dest)

            spec.blocks.install.append(
                'mkdir -p "%{{buildroot}}/%(dirname {0})"'.format(file_.dest)
            )
            spec.blocks.install.append(
                'cp -R %{{SOURCE0}}/{0} %{{buildroot}}/{1}'.format(
                    file_.src,
                    file_.dest,
                )
            )
            spec.blocks.files.append(file_directive)
            spec.blocks.post.append(
                'chown -R '
                '%{{file_permissions_user}}:%{{file_permissions_group}} '
                '/{0}'.format(file_.dest)
            )

        return spec
