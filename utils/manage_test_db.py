import os


def enable_test_db():
    if os.environ["TESTING"] != "True":
        os.environ["TESTING"] = "True"


def disable_test_db():
    if os.environ["TESTING"] != "False":
        os.environ["TESTING"] = "False"
