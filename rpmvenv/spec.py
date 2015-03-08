"""SPEC file interface and implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import copy

try:

    from ordereddict import OrderedDict

except ImportError:

    from collections import OrderedDict

from . import template


class Blocks(object):

    """Container for SPEC file blocks."""

    def __init__(self):
        """Initialize the blocks container."""
        self._blocks = {}

    def get(self, name):
        """Get the block content by name."""
        return self._blocks.setdefault(name, [])

    def add(self, name, line):
        """Add a line to a block by name."""
        return self.get(name).append(line)

    @property
    def post(self):
        """Get the post block."""
        return self.get('post')

    @property
    def postun(self):
        """Get the postun block."""
        return self.get('postun')

    @property
    def pre(self):
        """Get the pre block."""
        return self.get('pre')

    @property
    def preun(self):
        """Get the preun block."""
        return self.get('preun')

    @property
    def prep(self):
        """Get the prep block."""
        return self.get('prep')

    @property
    def build(self):
        """Get the build block."""
        return self.get('build')

    @property
    def install(self):
        """Get the install block."""
        return self.get('install')

    @property
    def clean(self):
        """Get the clean block."""
        return self.get('clean')

    @property
    def description(self):
        """Get the description block."""
        return self.get('description')

    @property
    def files(self):
        """Get the files block."""
        return self.get('files')

    def __iter__(self):
        """Iterate over the contained blocks."""
        for block_name, block_lines in self._blocks.items():

            yield (block_name, block_lines)


class Spec(object):

    """A SPEC file."""

    def __init__(self):
        """Initialize the SPEC file."""
        self.macros = OrderedDict()
        self.globals = OrderedDict()
        self.tags = OrderedDict()
        self.blocks = Blocks()

    def __str__(self):
        """Generate a string representation of the SPEC file."""
        return template.get('spec').render(spec=self)

    def __repr__(self):
        """Generate a readable representation of the SPEC file."""
        return str(self)

    def copy(self):
        """Generate a deep copy of the SPEC."""
        return copy.deepcopy(self)
