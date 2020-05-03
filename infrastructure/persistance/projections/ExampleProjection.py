# Third Party
from python_ddd.eventsourcing.Projection import MongoProjection


class ExampleProjection(MongoProjection):
    def __init__(self, client, event_publisher):
        super().__init__(client, collection="collection", database="database")
        event_publisher.register_listener(self)

    def project(self, obj_id, event_name, event):
        if (
            event_name == "password_recovery_token_created"
            and obj_id.startswith("User")
        ):
            # Fill me
            pass
