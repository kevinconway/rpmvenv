"""Extension for providing custom block segments."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import StringOption

from .. import interface


cfg = Configuration(
    blocks=Namespace(
        description='Add custom lines to any RPM block.',
        post=ListOption(
            description='Lines to add to %post.',
            option=StringOption(),
            default=(),
        ),
        postun=ListOption(
            description='Lines to add to %postun.',
            option=StringOption(),
            default=(),
        ),
        pre=ListOption(
            description='Lines to add to %pre.',
            option=StringOption(),
            default=(),
        ),
        preun=ListOption(
            description='Lines to add to %preun.',
            option=StringOption(),
            default=(),
        ),
        prep=ListOption(
            description='Lines to add to %prep.',
            option=StringOption(),
            default=(),
        ),
        build=ListOption(
            description='Lines to add to %build.',
            option=StringOption(),
            default=(),
        ),
        install=ListOption(
            description='Lines to add to %install.',
            option=StringOption(),
            default=(),
        ),
        clean=ListOption(
            description='Lines to add to %clean.',
            option=StringOption(),
            default=(),
        ),
    ),
)


class Extension(interface.Extension):

    """Extension which adds generic block additions."""

    name = 'blocks'
    description = 'Add custom lines to an RPM block.'

    @staticmethod
    def _append(mapping, name, lines):
        """Add a block into the mapping if lines are given."""
        for line in lines:

            mapping.setdefault(name, []).append(line)

        return mapping

    @classmethod
    def generate(cls, namespace):
        """Produce block segments from input."""
        blocks = {}
        blocks = cls._append(blocks, 'post', namespace.post)
        blocks = cls._append(blocks, 'postun', namespace.postun)
        blocks = cls._append(blocks, 'pre', namespace.pre)
        blocks = cls._append(blocks, 'preun', namespace.preun)
        blocks = cls._append(blocks, 'prep', namespace.prep)
        blocks = cls._append(blocks, 'build', namespace.build)
        blocks = cls._append(blocks, 'install', namespace.install)
        blocks = cls._append(blocks, 'clean', namespace.clean)

        return {
            "macros": (),
            "defines": (),
            "globals": (),
            "tags": (),
            "blocks": tuple(blocks.items()),
        }
