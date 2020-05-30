from pathlib import Path
from os import walk, getenv
import json
from platform import system, release, version


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
def load_all_permissions(file_type):
    modules_path = None

    if system() == "Windows":
        modules_path = Path('app', 'modules')
    elif system() == "Linux":
        modules_path = Path('/app', 'modules')

    if getenv("DEPLOY") == "Production":
        modules_path = './modules/'

    permissions = {}

    # TODO: [REFACTOR] Break up into generic FileLoader and FolderSearch
    # for root, dirs, files in walk(modules_path, topdown=True):
    for root, dirs, files in walk(modules_path, topdown=True):
        if file_type == "json":

            if "permissions.json" in files:

                file_path = root + "/permissions.json"

                with open(file_path, "r") as read_file:
                    data = json.load(read_file)
                    if len(data) > 0:
                        for key in data:
                            permissions[key] = data[key]

    return permissions
