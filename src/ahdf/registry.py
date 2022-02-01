import collections
import functools

from argcompile.utils import MustImplementError


class AbstractRegistry:
    """Generic two-level mapper helper class."""

    def __init__(self):
        self._content = collections.defaultdict(dict)

    def __getitem__(self, path):
        bucket, key = path
        return self._content[bucket][key]

    def __setitem__(self, path, value):
        bucket, key = path
        self._content[bucket][key] = value

    def __delitem__(self, path):
        bucket, key = path
        del self._content[bucket][key]

    def register(self, *args):
        """
        Allocate a given object in _content.
        This method can be used as a decorator or explicitly.
        """
        # Used as decorator
        if len(args) == 2:
            return functools.partial(self.__setitem__, args)

        bucket, key, obj = args
        self[bucket, key] = obj

    def get(self, bucket, key, default=None):
        try:
            return self.__getitem__((bucket, key))
        except KeyError:
            return default

    def __str__(self):
        output = ''
        for bucket, map in self._content.items():
            output += f'{bucket}:\n'

            for key, value in map.items():
                output += f'\t{key}: {value}\n'
        return output


class Registry(AbstractRegistry):
    """Object-oriented bucket allocation registry"""

    def register(self, *args):
        """
        Allocate a given object in _content.
        This method can be used as a decorator or explicitly.
        """
        # Used as decorator with implicit bucket
        if len(args) == 1:
            key, = args
            
            def registration(obj):
                bucket = self.bucketize(obj)
                self[bucket, key] = obj
            return registration

        return super(Registry, self).register(*args)

    def bucketize(self, obj):
        """A way to define, through obj, in which bucket it should be placed"""
        raise MustImplementError(self, 'bucketize')
