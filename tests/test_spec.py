"""Test suites for the Spec object."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from rpmvenv import spec


def test_spec_macros():
    """Test if macros are added and ordered."""
    specfile = spec.Spec()
    specfile.macros['test1'] = 'test1'
    specfile.macros['test2'] = 'test2'

    assert """%define test1 test1
%define test2 test2""" in str(specfile)


def test_spec_globals():
    """Test if globals are added and ordered."""
    specfile = spec.Spec()
    specfile.globals['test1'] = 'test1'
    specfile.globals['test2'] = 'test2'

    assert """%global test1 test1
%global test2 test2""" in str(specfile)


def test_spec_tags():
    """Test if tags are added and ordered."""
    specfile = spec.Spec()
    specfile.tags['test1'] = 'test1'
    specfile.tags['test2'] = 'test2'

    assert """test1: test1
test2: test2""" in str(specfile)


def test_spec_blocks():
    """Test if blocks are added and ordered."""
    specfile = spec.Spec()
    specfile.blocks.get('test1').extend((
        'test1',
        'test1',
    ))
    specfile.blocks.get('test2').extend((
        'test2',
        'test2',
    ))

    assert """%test1
test1
test1""" in str(specfile)

    assert """%test2
test2
test2""" in str(specfile)
