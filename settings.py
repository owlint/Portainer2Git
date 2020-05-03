"""Contains settings for this application"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PASSWORD_RECOVERY_EMAIL_TEMPLATE = os.getenv(
    "PASSWORD_RECOVERY_EMAIL_TEMPLATE", "password_recovery"
)
PASSWORD_RECOVERY_FRONT_URL = os.getenv(
    "PASSWORD_RECOVERY_FRONT_URL", "https://graphboard.owl-int.com/recovery"
)


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


def redis_url():
    return os.getenv("redis", "localhost")


def redis_password():
    return os.getenv("redis_password", None)


def redis_database():
    return int(os.getenv("redis_database", "0"))
