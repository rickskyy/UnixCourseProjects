import glob
import shutil
import os
from pathlib import Path


def find_files_by_extension(source_path, extension):
    source_files = [(Path(file).suffix, file) for file in glob.iglob(
        "{source_path}/*".format(source_path=source_path),
        recursive=False)
    ]

    result_files = filter(
        lambda file_tuple: file_tuple[0] == extension,
        source_files
    )

    return result_files


def move_files(result_files, destination_path):
    print("Copying to {destination_path}...".format(
        destination_path=destination_path)
    )

    total_bytes = 0
    total_count = 0
    for file_tuple in result_files:
        print(file_tuple[1])
        total_bytes += os.path.getsize(file_tuple[1])
        total_count += 1
        shutil.move(file_tuple[1], destination_path)

    total_size = total_bytes

    print("Copied successfully.")
    print("Total files count: {count}".format(count=total_count))
    print("Total files size: {size} KB".format(size=total_size))
