from typing import Union


class ExampleView:
    def __init__(self, client, database="database", collection="collection"):
        super().__init__()
        self.__client = client
        self.__db = self.__client[database]
        self.__collection = self.__db[collection]

    def user_id_for_token(self):
        # Fill me
        pass
