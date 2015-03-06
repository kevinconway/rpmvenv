"""Extensions which package files not typically in the buildroot."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import PatternOption
from confpy.api import StringOption

from .. import interface


cfg = Configuration(
    file_extras=Namespace(
        description='Add default file permissions to files in buildroot.',
        user=StringOption(
            description='The owner user.',
        ),
        group=StringOption(
            description='The owner group.',
        ),
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

    @staticmethod
    def generate(namespace):
        """Produce file block segments for setting permissions."""
        install = []
        files = []
        post = []
        if namespace.files:

            for file_ in namespace.files:

                src, dest = file_.split(':')
                install.append(
                    'mkdir -p "%{{buildroot}}/%(dirname {0})"'.format(dest)
                )
                install.append(
                    'cp -R %{{SOURCE0}}/{0} %{{buildroot}}/{1}'.format(
                        src,
                        dest,
                    )
                )
                files.append(
                    '/{0}'.format(dest)
                )

                if namespace.user and not namespace.group:

                    post.append(
                        'chown -R {0} /{1}'.format(namespace.user, dest)
                    )

                if namespace.user and namespace.group:

                    post.append(
                        'chown -R {0}:{1} /{2}'.format(
                            namespace.user,
                            namespace.group,
                            dest,
                        )
                    )

        return {
            "macros": (),
            "defines": (),
            "globals": (),
            "tags": (),
            "blocks": (
                ('files', files),
                ('install', install),
                ('post', post),
            ),
        }
