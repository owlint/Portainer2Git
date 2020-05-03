"""Contains settings for this application"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

NEXT_CHECK_INTERVAL = int(os.getenv("NEXT_CHECK_INTERVAL", 10))


def dev():
    return os.getenv("dev", "False") == "True"


def set_dev(dev: bool):
    os.environ["dev"] = str(dev)


def mongo_url():
    return os.getenv("mongo", "localhost")


def mongo_username():
    return os.getenv("mongo_username", None)


def mongo_password():
    return os.getenv("mongo_password", None)
