"""Extension which accounts for the core RPM metadata fields."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import Namespace
from confpy.api import StringOption
from confpy.api import ListOption

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
        release=StringOption(
            description=(
                'The release number for the RPM. Default is 1. '
                'Supports strings to let free usage of, for example, %{?dist}.'
            ),
            default='1',
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
                '%(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}'
                '-%{release}-XXXXXX)'
            ),
        ),
        buildarch=StringOption(
            description='The build architecture to use.',
            required=False
        ),
        requires=ListOption(
            option=StringOption(),
            default=(),
            description='Dependencies',
            required=False
        ),
        conflicts=ListOption(
            option=StringOption(),
            default=(),
            description='Conflicts',
            required=False
        ),
        obsoletes=ListOption(
            option=StringOption(),
            default=(),
            description='Obsoletes',
            required=False
        ),
        provides=ListOption(
            option=StringOption(),
            default=(),
            description='Virtual package',
            required=False
        ),
    ),
)


class Extension(interface.Extension):

    """Common core RPM metadata fields."""

    name = 'core'
    description = 'Complete the common core RPM metadata fields.'
    version = '1.0.0'
    requirements = {}

    @staticmethod
    def generate(config, spec):
        """Generate the core RPM package metadata."""
        name = config.core.name
        version = config.core.version
        release = config.core.release
        summary = config.core.summary
        group = config.core.group
        license = config.core.license
        url = config.core.url
        source = config.core.source
        buildroot = config.core.buildroot
        buildarch = config.core.buildarch
        requires = tuple(config.core.requires)
        conflicts = tuple(config.core.conflicts)
        obsoletes = tuple(config.core.obsoletes)
        provides = tuple(config.core.provides)

        spec.tags['Name'] = name
        spec.tags['Version'] = version
        spec.tags['Release'] = release
        spec.tags['BuildRoot'] = buildroot

        if requires:
            spec.tags['Requires'] = ', '.join(requires)

        if conflicts:
            spec.tags['Conflicts'] = ', '.join(conflicts)

        if obsoletes:
            spec.tags['Obsoletes'] = ', '.join(obsoletes)

        if provides:
            spec.tags['Provides'] = ', '.join(provides)

        if buildarch:

            spec.tags["BuildArch"] = buildarch

        if summary:

            spec.tags['Summary'] = summary

        if group:

            spec.tags['Group'] = group

        if license:

            spec.tags['License'] = license

        if url:

            spec.tags['Url'] = url

        if source:

            spec.tags['Source0'] = source

        spec.blocks.prep.append('rm -rf %{buildroot}/*')
        spec.blocks.clean.append('rm -rf %{buildroot}')

        return spec
