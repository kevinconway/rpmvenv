"""Test suites for the FileOption object."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from rpmvenv.extensions.files import option as file_opt


def test_parse_colon_delimited():
    parser = file_opt.FileOption()

    src = '/foo/bar'
    dest = '/etc/foo'

    rpm_file = parser.coerce('{0}:{1}'.format(src, dest))
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == src
    assert rpm_file.dest == dest
    assert rpm_file.file_type is None
    assert rpm_file.file_type_option is None


def test_parse_colon_delimited_invalid():
    parser = file_opt.FileOption()

    with pytest.raises(ValueError) as excinfo:
        parser.coerce('foobar')
    assert 'foobar' in str(excinfo.value)


def test_parse_dict_no_file_type():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo'
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type is None
    assert rpm_file.file_type_option is None


def test_parse_dict_no_file_type_explicit():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo',
        'config': 0,
        'doc': False
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type is None
    assert rpm_file.file_type_option is None
    assert rpm_file.file_attr is None


def test_parse_dict_doc_file():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo',
        'doc': 'foobar',  # anything truthy is okay, value is ignored
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type == 'doc'
    assert rpm_file.file_type_option is None


def test_parse_dict_config_file_no_option():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo',
        'config': True
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type == 'config'
    assert rpm_file.file_type_option is None


def test_parse_dict_file_with_attributes():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo',
        'attr': {
            "permissions": "0644",
            "user": "testuser"
        }
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type is None
    assert rpm_file.file_type_option is None
    assert rpm_file.file_attr == {
        "permissions": "0644",
        "user": "testuser",
        "group": "-"
        }


def test_parse_dict_config_file_with_option():
    parser = file_opt.FileOption()

    value = {
        'src': '/foo/bar',
        'dest': '/etc/foo',
        'config': 'noreplace'
    }

    rpm_file = parser.coerce(value)
    assert isinstance(rpm_file, file_opt.RpmFile)
    assert rpm_file.src == value['src']
    assert rpm_file.dest == value['dest']
    assert rpm_file.file_type == 'config'
    assert rpm_file.file_type_option == 'noreplace'


def test_parse_unknown():
    parser = file_opt.FileOption()

    value = object()

    with pytest.raises(TypeError):
        parser.coerce(value)
