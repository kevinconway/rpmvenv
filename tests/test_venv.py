"""Test suites for the python venv Extension."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import copy

from rpmvenv.spec import Spec
from rpmvenv.extensions.python import venv


def test_use_pip_install_off():
    ext = venv.Extension()
    config = copy.deepcopy(venv.cfg)
    spec = Spec()
    ext.generate(config, spec)
    assert '%{venv_python} setup.py install' in str(spec)


def test_use_pip_install_on():
    ext = venv.Extension()
    config = copy.deepcopy(venv.cfg)
    config.python_venv.use_pip_install = True
    spec = Spec()
    ext.generate(config, spec)
    assert '%{venv_pip} .' in str(spec)


class TestRemovePycache:
    cmd = r'find %{venv_dir} -type d -name "__pycache__" ' \
          r'-print0 | xargs -0 rm -rf'

    def test_remove_pycache_off(self):
        ext = venv.Extension()
        config = copy.deepcopy(venv.cfg)
        spec = Spec()
        ext.generate(config, spec)
        assert self.cmd not in str(spec)

    def test_remove_pycache_on(self):
        ext = venv.Extension()
        config = copy.deepcopy(venv.cfg)
        config.python_venv.remove_pycache = True
        spec = Spec()
        ext.generate(config, spec)
        assert self.cmd in str(spec)
