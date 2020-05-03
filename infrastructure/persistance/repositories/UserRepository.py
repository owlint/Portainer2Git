# Third Party
from python_ddd.eventsourcing.EventSourceRepository import (
    MongoEventSourceRepository,
)

# Application
from domain.User.User import User


class UserRepository(MongoEventSourceRepository):
    def __init__(self, client):
        super().__init__(client, database="user_manager")

    def create_blank_domain_object(self):
        return User("Undefined", "Undefined", "Undefined", "Undefined")
