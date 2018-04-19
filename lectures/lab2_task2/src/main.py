from sys import stdin

from src.move_files import move_files
from src.move_files import find_files_by_extension
from src.path_type import PathType
import os
import sys
import argparse

if __name__ == '__main__':
    SCRIPT_DESCRIPTION = ('Copy files with speific extension '
                          'from source path to destination path')

    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('source_path',
                        type=PathType(exists=True, type=PathType.DIR_TYPE),
                        help='Source directory for files should copy'
                        )
    parser.add_argument('destination_path',
                        type=PathType(exists=True, type=PathType.DIR_TYPE),
                        help='Destination directory for files filtered files'
                        )

    args = parser.parse_args()
    source_path = os.path.abspath(args.source_path)
    destination_path = os.path.abspath(args.destination_path)

    if source_path == destination_path:
        message = ("Copying denied. Source path '{source_path}' "
                   "is equal to destination path '{destination_path}'").format(
            source_path=source_path,
            destination_path=destination_path
        )
        print(message)
        sys.exit(1)

    print("Please, enter file extension: ", end=' ', flush=True)
    extension = sys.stdin.readline().strip()

    print("Searching files with extension {extension} ...".format(
        extension=extension)
    )

    result_files = find_files_by_extension(source_path, extension)

    if not result_files:
        print("No files with extension {extension} found.".format(
            extension=extension)
        )
        sys.exit()

    move_files(result_files, destination_path)
