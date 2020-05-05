# Third Party
from python_ddd.eventsourcing.Projection import MongoProjection


class PortainerCheckTimeProjection(MongoProjection):
    def __init__(self, client, event_publisher):
        super().__init__(
            client, collection="portainer_check_time", database="portainer2git"
        )
        event_publisher.register_listener(self)

    def project(self, obj_id, event_name, event):
        if event_name == "next_check_changed" and obj_id.startswith(
            "Portainer"
        ):
            if self.__is_already_projected(obj_id):
                self.collection.update_one(
                    {"portainer_id": obj_id}, {"$set": {"next_check": event}}
                )
            else:
                self.collection.insert_one(
                    {"portainer_id": obj_id, "next_check": event}
                )

    def __is_already_projected(self, portainer_id: str) -> bool:
        return (
            self.collection.count_documents({"portainer_id": portainer_id}) > 0
        )
