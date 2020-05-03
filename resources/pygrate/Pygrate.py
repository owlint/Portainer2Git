from pymongo import MongoClient
import os


class Pygrate:
    def __init__(self):
        self.__client = MongoClient(
            os.getenv("mongo", "localhost"),
            27017,
            username=os.getenv("mongo_username", None),
            password=os.getenv("mongo_password", None),
        )
        self.__db = self.__client["user_manager"]

    def get_migration_version(self):
        if self.__db.migrations.count() > 0:
            return list(self.__db.migrations.find())[0]["version"]
        else:
            return 0

    def set_migration_version(self, version):
        if self.__db.migrations.count() > 0:
            self.__db.migrations.delete_many({})
        self.__db.migrations.insert({"version": version})

    def get_seed_version(self):
        if self.__db.seeds.count() > 0:
            return list(self.__db.seeds.find())[0]["version"]
        else:
            return 0

    def set_seed_version(self, version):
        if self.__db.seeds.count() > 0:
            self.__db.seeds.delete_many({})
        self.__db.seeds.insert({"version": version})
