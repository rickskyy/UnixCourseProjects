import os
import glob
from pathlib import Path


def increment_parents(dirs, path_name):
    for name in dirs:
        if Path(name) in path_name.parents:
            dirs[name] += 1


def count_sub_dirs(search_path):
    dirs = {}
    for name in glob.glob(search_path + '/**', recursive=True):
        path_name = Path(name)
        if not os.path.isfile(name):
            dirs[name] = 0
        increment_parents(dirs, path_name)
    return ((key, dirs[key]) for key in sorted(dirs, key=dirs.__getitem__, reverse=True))
