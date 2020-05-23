from pathlib import Path
from os import walk
import json


def load_all_permissions(path):
    module_path = Path(path).parent / "modules/"

    permissions = {}

    for root, dirs, files in walk(module_path, topdown=True):

        if "permissions.json" in files:

            file_path = root + "/permissions.json"

            with open(file_path, "r") as read_file:
                data = json.load(read_file)
                if len(data) > 0:
                    for key in data:
                        permissions[key] = data[key]

    return permissions
