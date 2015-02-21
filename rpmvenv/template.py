"""Tools for fetching the JINJA2 templates."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import jinja2


ENV = jinja2.Environment(
    loader=jinja2.PackageLoader('rpmvenv', 'templates'),
)


def get(name):
    """Get a template from the built-in set or from an external path.

    Args:
        name (str): The name of the template to load. If the template does not
            match the name of a built-in template then it is assumed the value
            is a path to an external template file which will be loaded
            instead.

    Returns:
        Template: A jinja2 template object.

    Raises:
        jinja2.TemplateNotFound: If no template can be resolved.
    """
    try:

        return ENV.get_template(name)

    except jinja2.TemplateNotFound:

        package_dir = os.path.dirname(os.path.abspath(name))
        name = os.path.basename(name)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(package_dir),
        ).get_template(name)
