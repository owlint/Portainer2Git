# Third Party
from python_ddd.eventsourcing.EventSourceRepository import (
    MongoEventSourceRepository,
)

# Application
from domain.Portainer.Portainer import Portainer


class PortainerRepository(MongoEventSourceRepository):
    def __init__(self, client):
        super().__init__(client, database="portainer2git")

    def create_blank_domain_object(self):
        return Portainer("local", "http://test.com", "username", "password")
