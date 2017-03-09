"""Confpy extension that supports using RPM file paths as config options."""

from collections import MutableMapping, namedtuple

from confpy.core import option

try:
    basestring
except NameError:
    basestring = str

RpmFile = namedtuple('RpmFile',
                     ['src', 'dest', 'file_type', 'file_type_option'])


class FileOption(option.Option):

    """Configuration option used to insert file path mappings."""

    def coerce(self, value):
        """Convert dict or string values into RpmFile values.

        Supports structured dicts for more advanced directives or simple
        colon delimited strings for basic files.

        Args:
            value (str or dict): The value to coerce.

        Raises:
            TypeError: If the value is not a dict or string.
            ValueError: For dicts, if the value is missing a required key.
                        For strings, if the value is missing a colon.

        Returns:
            RpmFile: The RpmFile value represented.
        """
        if isinstance(value, MutableMapping):
            if 'src' not in value:
                raise ValueError('The value is missing the "src" key')
            if 'dest' not in value:
                raise ValueError('The value is missing the "dest" key')

            file_type = None
            file_type_option = None

            config_type = value.get('config', False)
            if config_type:
                file_type = 'config'
                if isinstance(config_type, basestring):
                    file_type_option = config_type
            elif value.get('doc', False):
                file_type = 'doc'

            return RpmFile(src=value['src'],
                           dest=value['dest'],
                           file_type=file_type,
                           file_type_option=file_type_option)

        elif isinstance(value, basestring):
            try:
                src, dest = value.split(':')
                return RpmFile(src=src,
                               dest=dest,
                               file_type=None,
                               file_type_option=None)
            except ValueError:
                raise ValueError('The value {0} is missing a :'.format(value))

        raise TypeError('Could not coerce {0} to an RpmFile'.format(value))
