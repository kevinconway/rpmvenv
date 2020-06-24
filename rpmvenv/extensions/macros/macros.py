"""Extension for packaging a Python virtualenv."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import ListOption
from confpy.api import Namespace
from confpy.api import StringOption
from confpy.api import BoolOption

from .. import interface


cfg = Configuration(
    macros=Namespace(
        macros=ListOption(
            description='Add global macros',
            option=StringOption()
        )
    )
)


class Extension(interface.Extension):

    """Extension for global macros"""

    name = 'macros'
    description = 'Packaging extension for global macros.'
    version = '1.0.0'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Generate Python virtualenv content."""
        for line in config.macros.macros:
            key, value = line.split(None, 1)
            spec.macros[key] = value
        return spec
