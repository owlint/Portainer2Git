import datetime


class PortainerCheckTimeView:
    def __init__(
        self,
        client,
        database="portainer2git",
        collection="portainer_check_time",
    ):
        super().__init__()
        self.__client = client
        self.__db = self.__client[database]
        self.__collection = self.__db[collection]

    def portainer_ids_to_check(self) -> bool:
        now = datetime.datetime.now().timestamp()
        cursor = self.__collection.find({"next_check": {"$lt": now}})
        documents = list(cursor)
        cursor.close()

        return [d["portainer_id"] for d in documents]
