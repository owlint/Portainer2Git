# Third Party
from python_ddd.eventsourcing.Projection import MongoProjection


class PortainerNameProjection(MongoProjection):
    def __init__(self, client, event_publisher):
        super().__init__(
            client, collection="portainer_name", database="portainer2git"
        )
        event_publisher.register_listener(self)

    def project(self, obj_id, event_name, event):
        if event_name == "name_changed" and obj_id.startswith("Portainer"):
            self.collection.insert_one({"obj_id": obj_id, "name": event})
