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


BLOCKS = (
    'post',
    'postun',
    'pre',
    'preun',
    'prep',
    'build',
    'install',
    'clean',
    'desc',
    'files',
    'changelog',
)


OPTIONS = dict(
    (block, ListOption(
        description='Lines to add to %{0}.'.format(block),
        option=StringOption(),
        default=(),
    ))
    for block in BLOCKS
)

cfg = Configuration(
    blocks=Namespace(
        description='Add custom lines to any RPM block.',
        **OPTIONS
    ),
)


class Extension(interface.Extension):

    """Extension which adds generic block additions."""

    name = 'blocks'
    description = 'Add custom lines to an RPM block.'
    version = '1.0.0'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Produce block segments from input."""
        for block in BLOCKS:

            lines = tuple(getattr(config.blocks, block))
            if lines:

                block_lines = None
                if block == 'desc':

                    block_lines = spec.blocks.get('description')

                else:

                    block_lines = spec.blocks.get(block)

                block_lines.extend(lines)

        return spec
