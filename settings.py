"""Contains settings for this application"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

NEXT_CHECK_INTERVAL = int(os.getenv("NEXT_CHECK_INTERVAL", 30))
PORTAINER_VALIDITY_TIMEOUT = int(os.getenv("PORTAINER_VALIDITY_TIMEOUT", 120))
VAULT_PASSWORD = os.environ["VAULT_PASSWORD"]
REMOTE_REPOSITORY = os.environ["REMOTE_REPOSITORY"]
REPOSITORY_BRANCH = os.getenv("REPOSITORY_BRANCH", "master")
LOCAL_REPOSITORY = os.getenv("LOCAL_REPOSITORY", "resources/portainers")


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
