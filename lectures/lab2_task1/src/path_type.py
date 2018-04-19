import os
from argparse import ArgumentTypeError


class PathType(object):

    FILE_TYPE = 'file'
    DIR_TYPE = 'dir'

    def __init__(self, exists=True, type=FILE_TYPE):
        assert exists in (True, False, None)
        assert type in (
            PathType.FILE_TYPE,
            PathType.DIR_TYPE,
            None
        ) or hasattr(type, '__call__')

        self.exists = exists
        self.type = type

    def __call__(self, string):
        is_exist = os.path.exists(string)
        if self.exists is True:
            if not is_exist:
                raise ArgumentTypeError("Path does not exist: '{path}'".format(path=string))
            elif (self.type == PathType.FILE_TYPE and
                  not os.path.isfile(string)):
                raise ArgumentTypeError(
                    "Path does not a file: '{path}'".format(path=string)
                )
            elif self.type == PathType.DIR_TYPE and not os.path.isdir(string):
                raise ArgumentTypeError(
                    "Path does not a directory: '{path}'".format(path=string)
                )
        else:
            if self.exists is False and is_exist:
                raise ArgumentTypeError("Path exists: '{path}'".format(path=string))
            parent_directory = os.path.dirname(os.path.normpath(string)) or '.'
            if not os.path.isdir(parent_directory):
                raise ArgumentTypeError(
                    "Parent path is not a directory: '{path}'".format(
                        path=string
                    )
                )
            elif not os.path.exists(parent_directory):
                raise ArgumentTypeError(
                    "Parent directory does not a exists: '{path}'".format(
                        path=string
                    )
                )
        return string
