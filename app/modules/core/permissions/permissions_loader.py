from pathlib import Path
from os import walk
import json


class FileLoader:
    """
    Load files from the system
    """
    def __init__(self,
                 file_type: str,
                 file_name: str,
                 file_path: str = None,
                 file_parser=None):
        # TODO: [UTIL] Implement generic file loader
        pass
    pass


class FolderSearcher:
    """
    Walk through folders on the filesystem.
    """
    # TODO: [UTIL] Implement generic folder searcher.
    pass


# TODO: [TEST] load_all_permissions()
def load_all_permissions(path, file_type):
    module_path = Path(path).parent / "modules/"

    permissions = {}

    # FIXME: Permissions loader doesn't work on Windows systems
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
