class PortainerNameView:
    def __init__(
        self, client, database="portainer2git", collection="portainer_name"
    ):
        super().__init__()
        self.__client = client
        self.__db = self.__client[database]
        self.__collection = self.__db[collection]

    def name_exists(self, name: str) -> bool:
        return self.__collection.count_documents({"name": name}) > 0
