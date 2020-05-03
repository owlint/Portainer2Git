import os

from pymongo import MongoClient, ASCENDING


class Migration:
    version = 1

    def __init__(self):
        self.__client = MongoClient(
            os.getenv("mongo", "localhost"),
            27017,
            username=os.getenv("mongo_username", None),
            password=os.getenv("mongo_password", None),
        )
        self.__db = self.__client["user_manager"]

    def apply(self):
        # Fill me
        pass

    def rollback(self):
        pass
