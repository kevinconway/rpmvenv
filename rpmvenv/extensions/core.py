"""Extension which accounts for the core RPM metadata fields."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import IntegerOption
from confpy.api import Namespace
from confpy.api import StringOption

from . import interface


cfg = Configuration(
    core=Namespace(
        description='Common core RPM metadata fields.',
        name=StringOption(
            description='The name of the RPM file which is generated.',
            required=True,
        ),
        version=StringOption(
            description='The RPM version to build.',
            required=True,
        ),
        release=IntegerOption(
            description='The release number for the RPM. Default is 1.',
            default=1,
        ),
        summary=StringOption(
            description='The short package summary.',
            required=False,
        ),
        group=StringOption(
            description='The RPM package group in which this package belongs.',
            required=False,
        ),
        license=StringOption(
            description='The license under which the package is distributed.',
            required=False,
        ),
        url=StringOption(
            description='The URL of the package source.',
            required=False,
        ),
        source=StringOption(
            description='The path to the package source.',
            required=False,
        ),
        buildroot=StringOption(
            description='The name of the buildroot directory to use.',
            default=(
                '%(mktemp -ud %{_tmppath}/%{name}-%{version}'
                '-%{release}-XXXXXX)'
            ),
        ),
    ),
)


class Extension(interface.Extension):

    """Common core RPM metadata fields."""

    name = 'core'
    description = 'Complete the common core RPM metadata fields.'

    @staticmethod
    def generate(namespace):
        """Generate the core RPM package metadata."""
        name = namespace.name
        version = namespace.version
        release = namespace.release
        summary = namespace.summary
        group = namespace.group
        license = namespace.license
        url = namespace.url
        source = namespace.source
        buildroot = namespace.buildroot

        tags = [
            ('Name', name),
            ('Version', version),
            ('Release', release),
            ('BuildRoot', buildroot),
        ]

        if summary:

            tags.append(('Summary', summary))

        if group:

            tags.append(('Group', group))

        if license:

            tags.append(('License', license))

        if url:

            tags.append(('Url', url))

        if source:

            tags.append(('Source0', source))

        return {
            "macros": (),
            "defines": (),
            "globals": (),
            "tags": tags,
            "blocks": (
                ('prep', ('rm -rf %{buildroot}/*',)),
                ('clean', ('rm -rf %{buildroot}',)),
            ),
        }
