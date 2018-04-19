from sys import stdin

from src.count_sub_dirs import count_sub_dirs
from src.path_type import PathType
import os
import argparse


if __name__ == '__main__':
    SCRIPT_DESCRIPTION = ('List all subdirectories of a given catalog, '
                          'sorted by the amount of children subdirectories and files.')

    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('catalog',
                        type=PathType(exists=True, type=PathType.DIR_TYPE),
                        help='Search directory'
                        )

    args = parser.parse_args()
    search_path = os.path.abspath(args.catalog)

    print("Please enter destination filename: ", flush=True)
    result_file_name = stdin.readline()

    dirs_tuple = count_sub_dirs(search_path)

    with open(result_file_name, "w") as result_file:
        for dir_name, children_number in dirs_tuple:
            result_file.write('{num}: {dir_name} \n'.format(num=children_number, dir_name=dir_name))
