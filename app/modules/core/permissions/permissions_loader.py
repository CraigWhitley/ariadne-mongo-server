from pathlib import Path
from os import walk
import json


class FileLoader:
    """
    Reusable class to load files from the system
    """
    pass


# TODO: [TEST] load_all_permissions()
def load_all_permissions(path, file_type):
    module_path = Path(path).parent / "modules/"

    permissions = {}
    # TODO: [REFACTOR] Break up into generic FileLoader and FolderSearch
    for root, dirs, files in walk(module_path, topdown=True):
        if file_type == "json":

            if "permissions.json" in files:

                file_path = root + "/permissions.json"

                with open(file_path, "r") as read_file:
                    data = json.load(read_file)
                    if len(data) > 0:
                        for key in data:
                            permissions[key] = data[key]

    return permissions
