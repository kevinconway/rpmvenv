"""Test suites for the primary entry point of the CLI."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from rpmvenv import cli


def test_cmd_build(source_code, config_file):
    """Test that a default build works without exception."""
    cfg = cli.load_configuration_file(config_file)
    extensions = cli.load_extensions(whitelist=cfg.extensions.enabled)
    mapping = cli.build_config(cfg, extensions)
    pkg = cli.build_from_mapping(mapping, source_code, cfg.core.name)
    assert cfg.core.name in pkg
