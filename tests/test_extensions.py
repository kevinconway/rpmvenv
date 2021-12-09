"""Test suites for the extension management features."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import itertools

from rpmvenv.extensions import loader


def test_loader_deterministic_order():
    """Test that the extensions are always loaded in requested order."""
    extensions = ("file_permissions", "file_extras", "python_venv", "blocks")
    for selection in itertools.permutations(extensions):
        results = loader.load_extensions(selection)
        results = (result.name for result in results if result.name != "core")
        assert tuple(results) == selection
